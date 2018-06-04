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
	
	self.menu_search = function() {
		//Note: we're probably going to need a function to get information from tables
		//match the college value to the database college location
		//after the match take the menu data from that college
		//Then match the search texts with the database menu

        //Need to add
		$.post(menu_search,
            {
                food_name: self.vue.form_food
            },
            function (data) {
                self.vue.menus = data.results;
            }
         )

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
			menu_is_eggs: 0,
            menu_is_fish: 0,
            menu_is_gluten_free: 0,
            menu_is_nuts: 0,
            menu_is_soy: 0,
            menu_is_vegan: 0,
            menu_is_vegetarian: 0,
            menu_is_pork: 0,
            menu_is_beef: 0,
            menu_is_halal: 0
        },
        methods: {
			menu_search: self.menu_search,
			filter_checkbox: self.filter_checkbox,
        }

    });

	$("vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
