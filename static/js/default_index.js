// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };
	
	function get_menu_url(start_idx, end_idx) {
		var pp = {
			start_idx: start_idx,
			end_idx: end_idx
		};
		
		return menu_url + "?" + $.param(pp);
	}
	
	self.get_memos = function() {
		$.getJSON(get_menu_url(0, 100), function (data) {
			//self.vue.menus = data.menus
			//possible way to get entire menu to the front end
	};
	
	self.do_search = function(search_input) {
		//Note: we're probably going to need a function to get information from tables
		//match the college value to the database college location
		//after the match take the menu data from that college
		//Then match the search texts with the database menu
		/*
		$.post(search_input_url,
            {
                searching: search_input
            },
		*/
	};
	
	self.college_checkbox = function(college_search) {
		//an idea for how the checkboxs should work
		if(college_search ==="nine_ten") {
			self.vue.nine_ten = !self.vue.nine_ten;
		}
		
		else if(college_search ==="cowell_stevenson") {
			self.vue.cowell_stevenson = !self.vue.cowell_stevenson;
		}
		
		else if(college_search ==="crown_merrill") {
			self.vue.crown_merrill = !self.vue.crown_merrill;
		}
		
		else if(college_search ==="porter_kresge") {
			self.vue.porter_kresge = !self.vue.porter_kresge;
		}
		
		else if(college_search ==="carson_oakes") {
			self.vue.carson_oakes = !self.vue.carson_oakes;
		}
		
		self.vue.college = college_search;
		
		/* ideally this is suppose to send the college name where the api wil do its work
		$.post(college_name_url,
            {
                college_name: college_search
            },
			*/
	};
	
	self.filter_checkbox = function(filter) {
		//an Idea for the checkbox for the menu
		if(filter ==="menu_is_eggs") {
			self.vue.menu_is_eggs = !self.vue.menu_is_eggs;
		}
		
		else if(filter ==="menu_is_fish") {
			self.vue.menu_is_fish = !self.vue.menu_is_fish;
		}
		
		else if(filter ==="menu_is_gluten_free") {
			self.vue.menu_is_gluten_free = !self.vue.menu_is_gluten_free;
		}
		
		else if(filter ==="menu_is_nuts") {
			self.vue.menu_is_nuts = !self.vue.menu_is_nuts;
		}
		
		else if(filter ==="menu_is_soy") {
			self.vue.menu_is_soy = !self.vue.menu_is_soy;
		}	
		
		else if(filter ==="menu_is_vegan") {
			self.vue.menu_is_vegan = !self.vue.menu_is_vegan;
		}	
		
		else if(filter ==="menu_is_vegetarian") {
			self.vue.menu_is_vegetarian = !self.vue.menu_is_vegetarian;
		}	
		
		else if(filter ==="menu_is_pork") {
			self.vue.menu_is_pork = !self.vue.menu_is_pork;
		}	
		
		else if(filter ==="menu_is_beef") {
			self.vue.menu_is_beef = !self.vue.menu_is_beef;
		}	
		
		else if(filter ==="menu_is_halal") {
			self.vue.menu_is_halal = !self.vue.menu_is_halal;
		}

		/*ideally sends the filter name specification for the api to do it work. 
		$.post(filter_url,
            {
                filter_options: filter
            },
			*/
	}
	
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
			menus: [],
			nine_ten: false,
			cowell_stevenson: false,
			crown_merrill: false,
			porter_kresge: false,
			carson_oakes: false,
			form_food: null,
			form_ingrediants: null,
			college: "",
			menu_is_eggs: false,
            menu_is_fish: false,
            menu_is_gluten_free: false,
            menu_is_nuts: false,
            menu_is_soy: false,
            menu_is_vegan: false,
            menu_is_vegetarian: false,
            menu_is_pork: false,
            menu_is_beef: false,
            menu_is_halal: false
        },
        methods: {
			do_search: self.do_search,
			college_checkbox: self.college_checkbox,
			filter_checkbox: self.filter_checkbox, 
			get_menu: self.get_menu
			
        }

    });
	
	self.get_memos();
	$("vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
