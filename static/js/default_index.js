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
	
	self.do_search = function(search_input) {
		//Note: we're probably going to need a function to get information from tables
		//match the college value to the database college location
		//after the match take the menu data from that college
		//Then match the search texts with the database menu
	};
	
	self.college_checkbox = function(college_search) {
		//an idea for how the checkboxs should work
		if(college_search ==="nine_ten") {
			self.vue.nine_ten = !self.vue.nine_ten;
			self.vue.college = college_search;
		}
		
		else if(college_search ==="cowell_stevenson") {
			self.vue.cowell_stevenson = !self.vue.cowell_stevenson;
			self.vue.college = college_search;
		}
		
		else if(college_search ==="crown_merrill") {
			self.vue.crown_merrill = !self.vue.crown_merrill;
			self.vue.college = college_search;
		}
		
		else if(college_search ==="porter_kresge") {
			self.vue.porter_kresge = !self.vue.porter_kresge;
			self.vue.college = college_search;
		}
		
		else if(college_search ==="carson_oakes") {
			self.vue.carson_oakes = !self.vue.carson_oakes;
			self.vue.college = college_search;
		}
		
	};
	
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
			results: [],
			nine_ten: false,
			cowell_stevenson: false,
			crown_merrill: false,
			porter_kresge: false,
			carson_oakes: false,
			form_food: null,
			form_ingrediants: null,
			college: ""
        },
        methods: {
			do_search: self.do_search,
			college_checkbox: self.college_checkbox
			
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
