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


    self.add_post = function () {
        $.post(add_post_url,
            {
                title: self.vue.form_title,
                content: self.vue.form_content//.replace(/(?:\r\n|\r|\n)/g, '\t\n')
            },
            function (data) {
                console.log(typeof(data.post))
                self.vue.posts.unshift(data.post);
                enumerate(self.vue.posts);
                self.button_toggle(self.vue.add_post_button);
                // clear form values
                console.log('form cleared');
                self.vue.form_title = null;
                self.vue.form_content = null;
            }
        );
    };

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

    self.get_user_name_email = function () {
        $.post(get_user_and_email_url,
            function (data) {
                self.vue.user_name = data.user_name,
                self.vue.user_email = data.user_email
            }
        );
    }


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
            posts: [],
            //contain:  id, title, content, author, date_created, date_updated, author_email, _idx(from enumerate())
            form_title: null,
            form_content: null,
            user_name: null,
            user_email: null
        },
        methods: {
            get_more: self.get_more,
            add_post: self.add_post,
            button_toggle: self.button_toggle,
            get_user_name_email: self.get_user_name_email
        }
    });


    Vue.component('post', {
        props: ['title', 'content', 'author', 'author_email',
                'date_created', 'date_updated', 'is_author_return_edit',
                'user_email', 'add_post_button', 'button_toggle'],
        template: ' <div>\
                    <div class="post_title">{{title}}</div>\
                    <div class="post_content">{{content}}\
                        <div  class="edit_icon" v-if="user_email==author_email">\
                            <a href="#" v-on:click="button_toggle(add_post_button)">\
                                <i class="fa fa-pencil icon"></i>\
                            </a>\
                            <a>\
                                <i class="fa fa-trash-o icon"></i>\
                            </a>\
                        </div>\
                    </div>\
                    <div class="meta">{{author}}</div>\
                    <div class="meta">{{date_created}}</div>\
                    <div class="meta">{{date_updated}}</div>\
                    </div>'
    }); // ***the delimiter in template does not change

    self.get_user_name_email();
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
