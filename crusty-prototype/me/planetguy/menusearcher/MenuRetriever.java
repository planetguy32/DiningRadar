package me.planetguy.menusearcher;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Serializable;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.Set;

import org.joda.time.DateTime;


public class MenuRetriever {
	
	public enum DiningHall{
		COWELL_STEVENSON("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=##M##%2F##D##%2F##Y##&locationNum=05&locationName=a&naFlag=1"),
		CROWN_MERRILL("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=##M##%2F##D##%2F##Y##&locationNum=20&locationName=a&naFlag=1"),
		PORTER_KRESGE("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=##M##%2F##D##%2F##Y##&locationNum=25&locationName=a&naFlag=1"),
		OAKES_CARSON("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=##M##%2F##D##%2F##Y##&locationNum=30&locationName=a&naFlag=1"),
		NINE_TEN("http://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=##M##%2F##D##%2F##Y##&locationNum=40&locationName=a&naFlag=1");
		public final String url;
		private DiningHall(String url){
			this.url=url;
		}
	}
	
	public enum Meal{
		BREAKFAST("Breakfast"),
		LUNCH("Lunch"),
		DINNER("Dinner"),
		LATE_NIGHT("Late Night");
		public final String name;
		private Meal(String name){
			this.name=name;
		}
	}

	private static List<String> getHTMLLines(String urlToRead) throws IOException {
		URL url = new URL(urlToRead);
		HttpURLConnection conn = (HttpURLConnection) url.openConnection();
		conn.setRequestMethod("GET");
		BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		List<String> result=new ArrayList<>();
		String line;
		while ((line = rd.readLine()) != null) {
			result.add(line);
		}
		rd.close();
		return result;
	}
	
	public static List<String> getMenuItems(DiningHall diningHall, Meal meal){
		return getMenuItems(diningHall, meal, new DateTime());
	}

	
	public static List<String> getMenuItems(DiningHall diningHall, Meal meal, DateTime date){
		try{
			int day=date.getDayOfMonth();
			int month=date.getMonthOfYear();
			int year=date.getYear();
			String realURL=diningHall.url.replaceAll("##M##", month+"").replaceAll("##D##", day+"").replaceAll("##Y##", year+"");
			List<String> htmlLines=getHTMLLines(realURL);
			Iterator<String> i=htmlLines.iterator();
			
			boolean isInRightMeal=false;
			List<String> menuItemsInRightMeal=new ArrayList<>();
			
			//Filter out a bunch of lines we don't care about
			while(i.hasNext()){
				String line=i.next();
				if(isInRightMeal && line.contains("menusamprecipes")){
					//Cut down recipe
					line=line.substring(86);
					line=line.replaceAll("</span></div>", "");
					menuItemsInRightMeal.add(line);
				} else if(line.contains("menusampmeals")){
					isInRightMeal = line.contains(meal.name);
				}
			}
			return menuItemsInRightMeal;
		}catch(Exception e){
			e.printStackTrace();
		}
		return null;
	}
	
	public static <T> List<T> sample(List<T> input, int n){
		Set<T> ls=new HashSet<T>();
		Random rand=new Random();
		if(input.size() <= n)
			return input;
		while(ls.size() < n){
			T t=input.get(rand.nextInt(input.size()));
			ls.add(t);
		}
		return new ArrayList<T>(ls);
	}
	
	private static class FoodTimeAndPlace implements Serializable {
		public final Meal meal;
		public final DiningHall diningHall;
		public final int days;
		public FoodTimeAndPlace(Meal meal, DiningHall hall, int days){
			this.meal=meal;
			this.diningHall=hall;
			this.days=days;
		}
		public int hashCode(){
			return  days*DiningHall.values().length*Meal.values().length
					+ meal.ordinal()*DiningHall.values().length 
					+ diningHall.ordinal() ;
		}
		public boolean equals(Object o){
			return o.hashCode() == hashCode();
		}
		public String toString(){
			return meal.ordinal() +"_@"+diningHall.ordinal()+" in "+days;
		}
	}
	
	public static HashMap<String, List<FoodTimeAndPlace>> collectFoods(){
		HashMap<String, List<FoodTimeAndPlace>> foodFinder=new HashMap<>();
		for(int i=0; i<7; i++){
			DateTime date=new DateTime().plusDays(i);
			for(Meal meal:Meal.values()){
				for(DiningHall hall:DiningHall.values()){
					List<String> foods=getMenuItems(hall, meal, date);
					FoodTimeAndPlace ftp=new FoodTimeAndPlace(meal, hall, i);
					for(String food:foods){
						food=food.toLowerCase();
						List<FoodTimeAndPlace> ftps=foodFinder.get(food);
						if(ftps == null){
							ftps=new ArrayList<>();
							foodFinder.put(food, ftps);
						}
						ftps.add(ftp);
					}
				}
			}
		}
		return foodFinder;
	}
	
	public static String readStdoutOf(Process proc) throws IOException{
		InputStream in = proc.getInputStream();
		StringBuilder result=new StringBuilder();
	    int c;
	    while ((c = in.read()) != -1) {
	    	result.append((char)c);
	    }
	    in.close();
	    return result.toString();
	}
	
	public static String readStderrOf(Process proc) throws IOException{
		InputStream in = proc.getErrorStream();
		StringBuilder result=new StringBuilder();
	    int c;
	    while ((c = in.read()) != -1) {
	      result.append((char)c);
	    }
	    in.close();
	    return result.toString();
	}
	
	public static String toTitleCase(String input) {
	    StringBuilder titleCase = new StringBuilder();
	    boolean nextTitleCase = true;

	    for (char c : input.toCharArray()) {
	        if (Character.isSpaceChar(c)) {
	            nextTitleCase = true;
	        } else if (nextTitleCase) {
	            c = Character.toTitleCase(c);
	            nextTitleCase = false;
	        }

	        titleCase.append(c);
	    }

	    return titleCase.toString();
	}

	
	public static void main(String[] args) throws IOException, InterruptedException{
		Process zenityWindow;
		zenityWindow=Runtime.getRuntime().exec("zenity --progress --pulsate");
		HashMap<String, List<FoodTimeAndPlace>> foodFinder=collectFoods();
		zenityWindow.destroyForcibly();
		while(true){
			zenityWindow=Runtime.getRuntime().exec(new String[]{
					"zenity",
					"--entry",
					"--title=Menu Search",
					"--text=Food to Search For:"});
			String query=readStdoutOf(zenityWindow);
			zenityWindow.waitFor();
			if(zenityWindow.exitValue() != 0)
				return;
			//Zenity leaves a trailing newline - remove that.
			query=query.substring(0, query.length()-1);
			String result="";
			System.out.println("foodFinder: "+foodFinder);
			for(String s:foodFinder.keySet()){
				System.out.println(s);
				System.out.println(s.contains(query));
				if(s.contains(query)){
					result += toTitleCase(s) + ": \\\n";
					List<FoodTimeAndPlace> ftps=foodFinder.get(s);
					for(FoodTimeAndPlace ftp:ftps){
						result += ftp.meal.name + " at "+toTitleCase(ftp.diningHall.name().toLowerCase().replace('_', ' ')) + " in "+ftp.days + " days\\\n";
					}
				}
			}
			
			zenityWindow.destroyForcibly();
			
			System.out.println("Result: "+result);
			zenityWindow=Runtime.getRuntime().exec(new String[]{"zenity","--info", "--title=Search results","--text", ""+result+"",
					"--width=600", "--height=400" });
			System.out.println(readStderrOf(zenityWindow));
			System.out.println(readStdoutOf(zenityWindow));
			zenityWindow.waitFor();
		}
	}

}
/*
nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=3%2F6%2F2018&locationNum=40&locationName=a&naFlag=1
nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=3%2F9%2F2018&locationNum=40&locationName= College+Nine+%26+Ten&naFlag=1
http://nutrition.sa.ucsc.edu/menuSamp.asp?locationNum=40&locationName=College+Nine+%26+Ten&sName=&naFlag=1&dtdate=3%2F4%2F2018


 */

