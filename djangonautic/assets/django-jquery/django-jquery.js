/*jshint esversion: 6 */
  $('.outside-hover').hide()
initialise = function() {

  $('.online-duration').each(function(index, value) {
    // less that 24 hours.
    var $start = $(`#time-${index+1}`).text();
    // var $createEnd = moment()
    // var $end = moment($createEnd).format("MM/DD/YYYY hh:mm:ss")
    // var $duration = moment.utc(moment($end).diff(moment($start))).format("HH:mm")
    let $minutes = moment().diff(moment($start), 'minutes');
    let $days = moment().diff(moment($start), 'days');
    let $hours = moment().diff(moment($start), 'hours');

    if ($hours === 0) {
      $(`#endtime-${index+1}`).text($minutes + " minutes"); // curent time
    } else if ($hours >= 0 && $days <= 1) {
      $(`#endtime-${index+1}`).text($hours + " Hours"); // curent time
    } else if ($days >= 2) {
      $(`#endtime-${index+1}`).text($days + " Days");
    }

  });

  var cu = $('#current-user').text();
  $(".in").each(function() {
    if ($(this).is(":contains('" + cu + "')")) {
      $(this).remove();

    }
  });
  $(".bs-modal").each(function() {
    $(this).modalForm({
      formURL: $(this).data('form-url')
    });
  });

};
$("#modal").on("hidden.bs.modal", function() {
  $(".modal-content").html("");
});
$(document).ready(function() {
  initialise();

});
$(window).on('load',function(){

$('#loadData').click();
});
$('#loadData').on('click', function() {
  console.log('loaded')
$('#siteloader').load('http://127.0.0.1:8000/chat/dialogs/{{user.get_username}}');
});

//update_profile.HTML
//('.form-control.date').datepicker({format: "dd.mm.yyyy"});
  $("#edit-avatar").on("click", function(e) {
    e.preventDefault();
    $(".avatar-sub-button").toggle(); // Shows

  });

  $("#upload-photo").click(function(e) {

    e.preventDefault();
    $("#id_profile-0-avatar").click();

  });
  $("#remove-photo").click(function(e) {
    $("#profile-0-avatar-clear_id").is(":checked");
    e.preventDefault();
    $("#profile-0-avatar-clear_id").click();

  });
  $("#id_profile-0-avatar").on("change", function(e) {
    var $form = $(this).closest("form");
    $form.find("input[name=form-1-submit]").click();
    e.preventDefault();
  });

  $("#profile-0-avatar-clear_id").on("change", function(e) {
    var $form = $(this).closest("form");
    $form.find("input[name=form-1-submit]").click();
  });



  var p = document.querySelectorAll("p");
  p[0].style.display = "none";
//  p[1].style.display = "none";



  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

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



  // form upload

  $("#id_ajax_upload_form").on('submit',function(e) {

    e.preventDefault();
    $form = $(this);
    var formData = new FormData(this);

    $.ajax({
      url: window.location.pathname,
      type: "POST",
      data: formData,
      action: "ajax",
      //csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      cache: false,
      dataType: "json",
      success: function(response) {
    alert(response.message)
      var igSrc="/media/"+response.url;
     $('#ajaxImage').attr("src",igSrc);
    $("#profile-0-avatar-clear_id").prop('checked', false);
$("#id_profile-0-avatar").val('');


      },
      error:function(response){
        alert(response.errors);
      },
      contentType: false,
      processData: false,
    });
return false
  });

// logged_in_user_list.HTML
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
var $cu = $('#current-user').text();
var ajaxSucceeded = false;
// setInterval(function() {
format_time = function() {
  $('.online-duration').each(function(index, value) {
    // less that 24 hours.
    var $start = $(`#time-${index+1}`).text();
    // var $createEnd = moment()
    // var $end = moment($createEnd).format("MM/DD/YYYY hh:mm:ss")
    // var $duration = moment.utc(moment($end).diff(moment($start))).format("HH:mm")
    let $minutes = moment().diff(moment($start), 'minutes');
    let $days = moment().diff(moment($start), 'days');
    let $hours = moment().diff(moment($start), 'hours');

    if ($hours === 0) {
      $(`#endtime-${index+1}`).text($minutes + " minutes"); // curent time
    } else if ($hours >= 0 && $days <= 1) {
      $(`#endtime-${index+1}`).text($hours + " Hours"); // curent time
    } else if ($days >= 2) {
      $(`#endtime-${index+1}`).text($days + " Days");
    }
  });
};
var childImg = "foo";
$.ajax({
  url: window.location.pathname,
  type: 'GET',
  data: {
    action: 'online_offline'
  },
  success: function(data) {
    ajaxSucceeded = true;
    // grab the inner html of the returned div
    // so you don't nest a new div#refresh-this-div on every call
    var html = $(data).find('#logged-in-users').html();
    $('#logged-in-users').html(html);

    if ($('body').hasClass('modal-open')) {
      $(".in").each(function() {
        if ($(this).is(":contains('" + cu + "')")) {
          $(this).remove();

        } else {
          return false;
        }
        format_time();
        return true;
      });


    } else {
      format_time();
      $(".in").each(function() {
        if ($(this).is(":contains('" + $cu + "')")) {
          $(this).remove();
          console.log($cu);
        }
      });
      $(".bs-modal").each(function() {
        $(this).modalForm({
          formURL: $(this).data('form-url')

        });
        $(this).click(function(){
           var childImg =  $(this).data('profile');
           var userName =  $(this).data('name');
          $("#currentUserImg").val(childImg);
          $("#currentUser").val(userName);

        });
      });

    }

  },
  error: function(data) {
    console.log("error");
    console.log(data);
  }

});

// }, 50000)

// timecards create
// $('.hide-show-append:last').hide();


function check(){
var $selectObject = [];
var $selectionID = [];
var $n = $('.form-row').length;

 for (var x = 0; x < $n; x++){
   $selectionID[x] = $("#id_payroll_set-"+[x]+"-payType").find(":selected").val();
   for (var i = 0; i < $n; i++){
       $selectObject[i] = document.getElementById("id_payroll_set-"+[i]+"-payType").getElementsByTagName("option");
       $selectObject[i][$selectionID[x]].disabled = true;
       if($selectObject[i][$selectionID[x]].selected == true){
         $selectObject[i][$selectionID[x]].disabled = false;
       }
   }
   console.log('selection',$selectionID[x])
 }

}
check();
disTimecardAddBtn()
function addRemoveButton() {
  var conditionRow = $('.form-row:last');
  conditionRow.find('.btn.add-form-row')
   .removeClass('btn-success').addClass('btn-danger')
   .removeClass('add-form-row').addClass('remove-form-row')
   .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');
};
$(document).on("change","select",function(){
  $("option[value=" + this.value + "]", this).attr("selected", true).removeAttr("disabled").siblings().removeAttr("selected")
check();
});
var conditionRow = $('.form-row:not(:last)');

conditionRow.find('.btn.add-form-row')
 .removeClass('btn-success').addClass('btn-danger')
 .removeClass('add-form-row').addClass('remove-form-row')
 .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');


addAremoveViewNames();
function addAremoveViewNames(){
  $('.add-form-row').each(function(){ // Loop through all inputs
    this.name = this.name.toString().replace('remove-model', 'add-model');  // Replace name

  });
  $('.remove-form-row').each(function(){ // Loop through all inputs
        this.name = this.name.toString().replace('add-model', 'remove-model');  // Replace name
  });
}
function updateElementIndex(el, prefix, ndx) {
 var id_regex = new RegExp('(' + prefix + '-\\d+)');
 var replacement = prefix + '-' + ndx;
 if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
 if (el.id) el.id = el.id.replace(id_regex, replacement);
 if (el.name) el.name = el.name.replace(id_regex, replacement);
};

function cloneMore(selector, prefix) {
 var newElement = $(selector).clone(true);
 var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
 newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
   var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
   var id = 'id_' + name;
   $(this).attr({
     'name': name,
     'id': id
   }).val('').removeAttr('checked');
 });
 newElement.find('label').each(function() {
   var forValue = $(this).attr('for');
   if (forValue) {
     forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
     $(this).attr({
       'for': forValue
     });
   }
 });
 total++;
 $('#id_' + prefix + '-TOTAL_FORMS').val(total);
 $(selector).after(newElement);
 var conditionRow = $('.form-row:not(:last)');
 conditionRow.find('.btn.add-form-row')
   .removeClass('btn-success').addClass('btn-danger')
   .removeClass('add-form-row').addClass('remove-form-row')
   .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');

   disTimecardAddBtn();
 return false;
}

function deleteForm(btn) {

 var total = parseInt($('#id_payroll_set-TOTAL_FORMS').val());
 if (total > 1) {
   btn.closest('.form-row').remove();
   var forms = $('.form-row');
   $('#id_payroll_set-TOTAL_FORMS').val(forms.length);
   for (var i = 0, formCount = forms.length; i < formCount; i++) {
     $(forms.get(i)).find(':input').each(function() {
       updateElementIndex(this, i);
     });
   }
 }
 return false;

}

function disTimecardAddBtn (){
  var $n = $('.form-row').length -1;
  console.log($n);
  var $getDefaultVal = $('#initial-payroll_set-0-id_payroll_set-0-startTime').val();
  for(var x = 0; x < $n+1; x++){
    $('#initial-payroll_set-'+x+'-id_payroll_set-'+x+'-startTime').val($getDefaultVal);
    $('#id_payroll_set-'+x+'-startTime').val($getDefaultVal);
  }
   if ($n === 3){
     addRemoveButton();
     addAremoveViewNames();
   }
   else if($n+1 === 5){
       $('.form-row:last').remove();
        $('#id_payroll_set-TOTAL_FORMS').val(4);
   }
}

disTimecardAddBtn();
$(document).on('click', '.add-form-row', function(e) {
 // e.preventDefault();
 // cloneMore('.form-row:last', 'form');
 // $(this).siblings(".background-append").removeAttr("style");
 // return false;
});
$(document).on('click', '.remove-form-row', function(e) {
 // e.preventDefault();
 // deleteForm($(this));
 // return false;
});
// caluclate totals/validtae - front end
let daysArray = ["mon","tue","wed","thu","fri","sat","sun"];
var $val = '';
var $foo ='';



function doneEdit(index){
  $('.done-time').each(function(index){
    $(this).click(function(){
    for(var x = 0; x < daysArray.length; x++){
      $("#id_payroll_set-"+index+"-"+daysArray[x]+"Time").attr('disabled', 'disabled');
      calculateFields(index)
    }
    });
  });

}
function edit(index){
  $('.edit-time').each(function(index){
    $(this).click(function(){
    $('#id_payroll_set-'+index+'-totalTime').val('0'); //reset value add edit button
    for(var x = 0; x < daysArray.length; x++){
      $("#id_payroll_set-"+index+"-"+daysArray[x]+"Time").removeAttr('disabled');
    }
    });
  });
}


function disableInput(index){
  for(var x = 0; x < daysArray.length; x++){
    $("#id_payroll_set-"+index+"-"+daysArray[x]+"Time").attr('disabled', 'disabled');

  }
}
// function calculateFieldsOnChange(index){
//
//   for(var x = 0; x < daysArray.length; x++){
//      $("#id_payroll_set-"+index+"-"+daysArray[x]+"Time").change(function(){
//        $selVal = $("#id_payroll_set-"+index+"-payType").find(":selected").val();
//
//        $val = $(this).val();
//        $getTotal = $('#id_payroll_set-'+index+'-totalTime').val();
//        $total = parseInt($getTotal) + parseInt($val);
//        $('#id_payroll_set-'+index+'-totalTime').val($total).change();
//        if($selVal == 0){ // EPL
//          $foo = Null;
//        }
//        else if($selVal == 1){
//          $foo = 10; // EPL
//        }
//        else if($selVal == 2){
//          $foo = 40; // VAC
//        }
//        else if($selVal == 3){
//          $foo = 25; //SIC
//        }
//        // total amount can't excede balance.-- validate
//        if($total >$foo){
//          alert("you've exceded the amount!");
//        }
//     });
//   }
// }
function calculateFields(index){
$total = 0;
  for(var x = 0; x < daysArray.length; x++){
$("#id_payroll_set-"+index+"-"+daysArray[x]+"Time").each(function(){
 $val = $(this).val();
  $total += parseInt($val);
  $('#id_payroll_set-'+index+'-totalTime').val($total).change();

})




  }
}
$(".form-row").each(function(index){
// disableInput(index);
var g = $(this).index()
calculateFieldsOnChange(g);
doneEdit(g);
edit(g);
});
