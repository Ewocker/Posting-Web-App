// This is the js for the default/index.html view.

var app = function () {

    var self = {};

    Vue.config.silent = false; // show all warnings


    //---------------HELPER-----------------

    // Extends an array
    self.extend = function (a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    var enumerate = function (v) {
        var k = 0;
        return v.map(function (e) {
            e._idx = k++;
        });
    };


    function get_posts_url(start_idx, end_idx) {
        var param = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return get_more_posts_url + "?" + $.param(param);
    }

    //---------------------------------------

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        var add_posts_num = 4;
        $.getJSON(get_posts_url(num_posts, num_posts + add_posts_num),
            function (data) {
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
            self.extend(self.vue.posts, data.posts);
            enumerate(self.vue.posts);
        });
    };

    self.button_toggle = function (button) {
        button.display = !button.display
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            logged_in: false,
            has_more: false,
            add_post_button: {  //using dict.attr can pass by reference
                display: true
            },
            posts: []
        },
        methods: {
            get_more: self.get_more,
            button_toggle: self.button_toggle
        }
    });

    Vue.component('post', {
        props: ['title', 'content', 'author', 'date_created', 'date_updated'],
        template: ' <div>\
                    <div class="post_title">{{title}}</div>\
                    <div class="post_content">{{content}}</div>\
                    <div class="meta">{{author}}</div>\
                    <div class="meta">{{date_created}}</div>\
                    <div class="meta">{{date_updated}}</div>\
                    </div>'
    }); //the delimiter in template does not change


    self.get_more(0, 4);
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function () {
    APP = app();
});
