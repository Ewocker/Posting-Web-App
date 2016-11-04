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

    self.action = function (id) {
        if (id == 0) {
            self.vue.action_post = 0;
        } else {
            self.vue.action_post = id;
        }
    };

    self.add_or_edit = function () {
        if (self.vue.action_post == 0) {
            self.add_post();
        } else {
            self.update_post();
        }
    };

    self.disable_edit = function () {
        self.vue.editing = true;
    };
    self.enable_edit = function () {
        self.vue.editing = false;
    };

//Does not need to be a vue object method but it might be so leave it here
    self.add_post = function () {
        $.post(add_post_url,
            {
                title: self.vue.form_title,
                content: self.vue.form_content//.replace(/(?:\r\n|\r|\n)/g, '\t\n')
            },
            function (data) {
                console.log('add post success');
                self.vue.posts.unshift(data.post);
                enumerate(self.vue.posts);
                self.vue.action_post = 0;
                self.button_toggle(self.vue.add_post_button);
                // clear form values
                console.log('form cleared');
                self.clear_form();
            }
        );
    };

    self.update_post = function () {
        $.post(update_post_url,
            {
                title: self.vue.form_title,
                content: self.vue.form_content,//.replace(/(?:\r\n|\r|\n)/g, '\t\n')
                id: self.vue.action_post
            },
            function (data) {
                console.log(self.vue.action_post + ' success');
                for (i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id == data.post.id) {
                        self.vue.posts[i] = data.post;
                        break;
                    }
                }
                enumerate(self.vue.posts); // do not need but leave it
                self.button_toggle(self.vue.add_post_button);
                // clear form values
                console.log('form cleared');
                self.clear_form();
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
        button.display = !button.display;
    };

    self.get_user_name_email = function () {
        $.post(get_user_and_email_url,
            function (data) {
                self.vue.user_name = data.user_name,
                    self.vue.user_email = data.user_email
            }
        );
    };

    self.edit_post = function (title, content) {
        self.button_toggle(self.vue.add_post_button);
        self.vue.form_title = title;
        self.vue.form_content = content;
        self.vue.editing = !self.vue.editing;
        if (self.vue.editing == false) {
            self.vue.form_title = null;
            self.vue.form_content = null;
        }
    };

    self.delete_post = function (id) {
        $.post(del_post_url,
            {
                id: id
            },
            function () {
                console.log(self.vue.action_post + 'delete success');
                for (i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id == id) {
                        self.vue.posts.splice(i, 1);
                        break;
                    }
                }
                enumerate(self.vue.posts);
            }
        );
    };

    self.clear_form = function () {
        self.vue.form_title = null;
        self.vue.form_content = null;
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
            posts: [],
            //contain:  id, title, content, author, date_created, date_updated, author_email, _idx(from enumerate())
            editing: false,
            action_post: 0,
            form_title: null,
            form_content: null,
            user_name: null,
            user_email: null
        },
        methods: {
            get_more: self.get_more,
            add_post: self.add_post,
            button_toggle: self.button_toggle,
            get_user_name_email: self.get_user_name_email,
            edit_post: self.edit_post,
            clear_form: self.clear_form,
            disable_edit: self.disable_edit,
            enable_edit: self.enable_edit,
            action: self.action,
            add_or_edit: self.add_or_edit,
            delete_post: self.delete_post
        }
    });


    Vue.component('post', {
        props: ['post',
            'user_email',
            'date_created',
            'edit_post',
            'clear_form',
            'editing',
            'action',
            'delete_post'],
        template: ' <div class="post-content">\
                    <div class="post_title">{{post.title}}</div>\
                    <div class="post_content">{{post.content}}\
                        <div  class="edit_icon" v-if="user_email==post.author_email">\
                            <a href="#" v-on:click="edit_post(post.title, post.content); action(post.id); " v-if="!editing">\
                                <i class="fa fa-pencil icon"></i>\
                            </a>\
                            <a href="#" v-on:click="delete_post(post.id);">\
                                <i class="fa fa-trash-o icon"></i>\
                            </a>\
                        </div>\
                    </div>\
                    <div class="meta">{{post.author}}</div>\
                    <div class="meta">{{post.date_created}}</div>\
                    <div class="meta">{{post.date_updated}}</div>\
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
