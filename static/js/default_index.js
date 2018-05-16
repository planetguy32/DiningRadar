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
	
	function do_search_url() {
	}
	
	self.do_search = function() {
	};
	
	self.get_more_results = function () {
    };
	
	self.college_checkbox = function(college) {
		//an idea for how the checkboxs should work
		if(college ==="nine_ten") {
			self.vue.nine_ten = !self.vue.nine_ten
		}
		
		else if(college ==="cowell_stevenson") {
			self.vue.cowell_stevenson = !self.vue.cowell_stevenson
		}
		
		else if(college ==="crown_merrill") {
			self.vue.crown_merrill = !self.vue.crown_merrill
		}
		
		else if(college ==="porter_kresge") {
			self.vue.porter_kresge = !self.vue.porter_kresge
		}
		
		else if(college ==="carson_oakes") {
			self.vue.carson_oakes = !self.vue.carson_oakes
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
			get_more_results: self.get_more_results,
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
