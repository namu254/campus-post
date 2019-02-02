// protect against csrf
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// profile color changing script
var myVar;
function changeColor(){
  var fill_color = '#'+(Math.random()*0xFFFFFF<<0).toString(16);
  $("circle").attr('style', "fill:"+fill_color).fadeTo("slow", 0.8);
  myVar = setTimeout("changeColor()",1000);
}
$(document).ready(function(){
  changeColor();
});

  // start of jquery script
  //like script

  $(document).ready(function(){
  $(".like").click(function(){
    var id = $(this).attr("id");
    var like_count = $(this).find('span');
    var like_icon = $(this).find('i');
    $.ajax({
      url: '/like/' + id,
      success:function(data){
        like_count.text(data.like_count);
        if(data.is_like){
          like_icon.css("color", "red");
          like_count.css("color", "red");
        } else{
          like_icon.css("color", "#767676");
          like_count.css("color", "#767676");
        }    
      },
      error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("You are offline");

      window.setTimeout(response_hide, 2000);
      function response_hide() {
        $('.response').text("");
      }
    } 
    })
  });



  // looping through elements to check if the post has an like on that user
  $('.like').each(function(){
    var id = this.id;
    var icon = $(this).find('i');
    var like_count = $(this).find('span');
    $.ajax({
      url: '/check_like/' + id,
      success:function(data){
        like_count.text(data.like_count)
        if(data.is_like){
           icon.css("color", "red");
           like_count.css("color", "red");
          }
      }
    })
  });


  $('.name').click(function(event){
    window.location ="/";
  })



// Account creation 
$('.sign_up').on('submit', function(event){
  event.preventDefault();
  var username = $('#id_username').val();
  var email = $('#id_email').val();
  var password = $('#id_password').val();
  var university = $('#id_university').val();

  $('.response').css("background-color", "#000000");
  $('.response').text("Creating account...");
  $.ajax({
    url: '/sign_up',
    type: 'POST',
    data: { username: username,
            email: email,
            password:password,
            university:university
    },
    success:function(data){
      $("#id_password").val('');
      if(data.username_exists){
        $('#id_username').css("border", "1px solid red");
        $('.response').css("background-color", "red");
        $('.response').text("Username already exists");
      } else if (data.created){
        $('#id_username').css("border", "1px solid #4CAF50");
        $('.response').css("background-color", "#4CAF50");
        $('.response').html("Your account has been created. <a href='accounts/login/' style='color: white;text-decoration: underline'>You need to login now</a>");
        window.setTimeout(reload_page, 5000);
        function reload_page() {
            window.location = "/accounts/login/";
          }
      } 
    },
    error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed");
    }
  });
});

  // get user interests from the server 
  var user_interests = [];
  $(document).ready(function(){ 
    var i;
    $.ajax({
      url: '/get_interests',
      async: false,
      success:function(data){
        var i;
        var l = data.length;
        for(i=0;i<l;++i){
          user_interests.push(data[i]);
        }
      } 
    })
    // looping through the DOM highlighting the user interests
    $('.interest_container').each(function(){
      var id = this.id;
      var this_container = $(this);
      var i;
      var l = user_interests.length;
      for(i=0;i<l;++i){
          if(user_interests[i] === id){
            this_container.addClass('interest_container_selected');
          }
        }
    });
  });

// select the interest
$('.interest_container').click(function(){
  console.log("clicked")
    var id = this.id;
  if($(this).hasClass("interest_container_selected")){
    // remove interest from the array && not the last element in the array(pop)
    $(this).removeClass("interest_container_selected");
    user_interests = jQuery.grep(user_interests,function(value){
      return value != id;
    });
  } else{
    // add interest to the array (at the end) 
     $(this).addClass("interest_container_selected");
     user_interests.push(id);
  }
  var selected = user_interests.length;
  $('.response').css("background-color", "#000000");
  $('.response').text(selected + " interests selected" );
});



// Send the interests changes the server
$('.save_changes').click(function(){
  var final = user_interests;
  $('.response').css("background-color", "#000000");
  $('.response').text("Updating interest...");
  $.ajax({
  url: '/edit_interests',
  type: 'POST',
  data: {'data':final},
  success:function(data){
    if(data.changes_saved){
      $('.response').css("background-color", "#4CAF50");
        $('.response').text("Interests saved");
    }
    window.setTimeout(reload_page, 1000);
      function reload_page() {
          window.location = "/";
        } 
  },
  error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed");
    }
});
})

// navigate to interest page

$('.interest_tag').click(function(){
  var id = this.id;
  window.location ="interest/"+id;
});

// submit post 
$('.post_form').on('submit', function(event){
  event.preventDefault();
  
  var post_text = $('#post_text').val();
  var interest = this.id;
  $('.response').css("background-color", "#000000");
  $('.response').text("Posting...");
  $.ajax({
    url: '/add_post',
    type: 'POST',
    data: { post_text: post_text,
            interest: interest
    },
    success:function(data){
      $("#post_text").val('');
      if(data.saved){
        $('.response').css("background-color", "#4CAF50");
        $('.response').text("Post saved");
      } 
      window.setTimeout(reload_page, 1000);
      function reload_page() {
          window.location = "/interest/"+interest;
        }  
    },
    error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed");
    }
  });
});


// handle submit interest
$('.submit_interest').on('submit', function(event){
  event.preventDefault();
  var interest_name = $('#interest_name').val();
  var interest_description = $('#interest_description').val();
  
  $('.response').css("background-color", "#000000");
  $('.response').text("Submitting...");
  $.ajax({
    url: '/submit_interest',
    type: 'POST',
    data: { interest_name: interest_name,
            interest_description: interest_description
    },
    success:function(data){
      $("#interest_name").val('');
      $("#interest_description").val('');
      if(data.saved){
        $('.response').css("background-color", "#4CAF50");
        $('.response').text("Your interest has been submitted");
      } 
      window.setTimeout(reload_page, 2000);
      function reload_page() {
          window.location = "/";
        }  
    },
    error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed");
    }
  });
});


// Handle delete post
$('.delete_post').click(function(){
var post_id = this.id;
  $('.response').css("background-color", "#000000");
  $('.response').text("Deleting post...");
  $.ajax({
    url: '/delete_post/'+post_id,
    success:function(data){
      if(!data.is_deleted){
        $('.response').css("background-color", "#4CAF50");
        $('.response').text("Post deleted");
      }
      window.setTimeout(reload_page, 1000);
      function reload_page() {
          window.location = "/my_posts";
        } 
    },
    error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed to delete post");
    }
  });
});

// Handle recent interests
$('.recent_interest_tag').click(function(){
  var id = this.id;
  window.location ="interest/"+id;
});


// Handle commment section 
$('.view_comments').click(function(){
  var id = this.id;
  var this_box = $('#comment_box_'+id);

  if(this_box.hasClass("comment_box")){

    this_box.removeClass("comment_box");
    this_box.addClass("comment_show");
    
  }else{
    this_box.removeClass("comment_show");
    this_box.addClass("comment_box");
  }
});

// opening and closing of profile modal
$('.profile_icon').click(function(){
  $('.modal').css("display", "block");
});
$('.profile_close').click(function(){
  $('.modal').css("display", "none");
});


// opening and closing of delete account modal
$('.delete_account').click(function(){
  $('.del_acc_modal').css("display", "block");
});
$('.del_acc_close').click(function(){
  $('.del_acc_modal').css("display", "none");
});


// add_interest

$('.add_interest').click(function(){
  var interest = this.id;
  var action = $('.add_interest').text();
  $('.response').css("background-color", "#000000");
  $('.response').text("Updating...");
  $.ajax({
    url: '/add_interest',
    data: {interest: interest,action: action},
    success:function(data){
      if (data.interest == "added"){
        $('.add_interest').text("Remove");
        $('.users_count').text(data.users_count + " users");
        $('.response').css("background-color", "#4CAF50");
        $('.response').text(interest + " has been added to your interests");

        window.setTimeout(response_hide, 2000);
        function response_hide() {
          $('.response').text("");
        } 
      } else if(data.interest == "removed"){
        $('.add_interest').text("Add");
        $('.users_count').text(data.users_count + " users");
        $('.response').css("background-color", "red");
        $('.response').text(interest + " has been removed to your interests");
        window.setTimeout(response_hide, 2000);
        function response_hide() {
          $('.response').text("");
        }
      }
    },
    error:function(xhr,errmsg,err){
      $('.response').css("background-color", "red");
      $('.response').text("Failed");
    } 
  });
});


// change Password
$('.change_password').on('submit', function(event){
  event.preventDefault();
  var password = $('#id_new_password').val();
  var confirm_password = $('#id_confirm_password').val();
  
  $('.response').css("background-color", "#000000");
  $('.response').text("Changing...");

  if (password == confirm_password){
    $.ajax({
      url: '/change_password',
      type: 'POST',
      data: { password: password},
      success:function(data){
        $("#id_new_password").val('');
        $("#id_confirm_password").val('');
        if(data.changed){
          $('#id_new_password').css("border", "1px solid #4CAF50");
          $('#id_confirm_password').css("border", "1px solid #4CAF50");
          $('.response').css("background-color", "#4CAF50");
          $('.response').text("Your password has been changed");
        } 
        window.setTimeout(reload_page, 3000);
        function reload_page() {
            window.location = "/accounts/logout/";
          }  
      },
      error:function(xhr,errmsg,err){
        $('.response').css("background-color", "red");
        $('.response').text("Failed");
      }
    });
  } else {
    $('#id_new_password').css("border", "1px solid red");
    $('#id_confirm_password').css("border", "1px solid red");
    $('.response').css("background-color", "red");
    $('.response').text("Password does not match");
  }

});



});

 // End of jquery script
