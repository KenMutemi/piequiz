$(document).ready(function() {
  $('input[type="radio"]').keydown(function(e) {
    var arrowKeys = [37, 38, 39, 40];
    if (arrowKeys.indexOf(e.which) !== -1)
    {
        $(this).blur();
        if (e.which == 38)
        {
            var y = $(window).scrollTop();
            $(window).scrollTop(y - 10);
        }
        else if (e.which == 40)
        {
            var y = $(window).scrollTop();
            $(window).scrollTop(y + 10);
        }
        return false;
    }
  });

$('input[type=radio]').click(function() {
  $(this).closest("form").submit();
});

  $('.heading-collapse').click(function() {
    $(this).toggleClass('active').find('i').toggleClass('fa fa-chevron-up fa fa-chevron-down')
           .removeClass('active').find('i').removeClass('fa fa-chevron-up').addClass('fa fa-chevron-down');
         });

  $(".questions-preview").click(function(e){
    e.preventDefault();
    $(this).find(".popup").fadeIn("slow");
});

$(".new-password").dialog({modal: true, dialogClass: 'no-close password-dialog'});

    $(".vote_form").submit(function(e) 
    {
        e.preventDefault(); 
        var btn = $(".approve", this);
        var l_id = $(".hidden_id", this).val();
        btn.attr('disabled', true);
        $.post("/vote/", $(this).serializeArray(),
        function(data) {
            if(data["voteobj"]) {
          btn.text("Downvote");
            }
            else {
          btn.text("Upvote");
            }
        });
        btn.attr('disabled', false);
    });

      /** ajax for the test*/
    var test_form = $('.test-form');
    test_form.submit(function () {
        $.ajax({
            type: test_form.attr('method'),
            url: test_form.attr('action'),
            data: test_form.serialize(),
            success: function (data) {
            },
            error: function(data) {
                alert(JSON.stringify(data));
            }
        });
        return false;
    });

  window.autocomplete = new Autocomplete({
        form_selector: '#search'
      })
      window.autocomplete.setup()

    })


        // In a perfect world, this would be its own library file that got included
    // on the page and only the ``$(document).ready(...)`` below would be present.
    // But this is an example.
    var Autocomplete = function(options) {
      this.form_selector = options.form_selector
      this.url = options.url || '/search/autocomplete/'
      this.delay = parseInt(options.delay || 300)
      this.minimum_length = parseInt(options.minimum_length || 3)
      this.form_elem = null
      this.query_box = null
    }

    Autocomplete.prototype.setup = function() {
      var self = this

      this.form_elem = $(this.form_selector)
      this.query_box = this.form_elem.find('input[name=q]')

      // Watch the input box.
      this.query_box.on('keyup', function() {
        var query = self.query_box.val()

        if(query.length < self.minimum_length) {
          return false
        }

        self.fetch(query)
      })

      // On selecting a result, populate the search field.
      this.form_elem.on('click', '.ac-result', function(ev) {
        self.query_box.val($(this).text())
        $('.ac-results').remove()
        return false
      })
    }

    Autocomplete.prototype.fetch = function(query) {
      var self = this

      $.ajax({
        url: this.url
      , data: {
          'q': query
        }
      , success: function(data) {
          self.show_results(data)
        }
      })
    }

    Autocomplete.prototype.show_results = function(data) {
      // Remove any existing results.
      $('.ac-results').remove()

      var results = data.results || []
      var results_wrapper = $('<div class="ac-results"></div>')
      var base_elem = $('<div class="result-wrapper"><a href="#" class="ac-result"></a></div>')

      if(results.length > 0) {
        for(var res_offset in results) {
          var elem = base_elem.clone()
          // Don't use .html(...) here, as you open yourself to XSS.
          // Really, you should use some form of templating.
          elem.find('.ac-result').text(results[res_offset])
          results_wrapper.append(elem)
        }
      }
      else {
        var elem = base_elem.clone()
        elem.text("")
        results_wrapper.append(elem)
      }

      this.query_box.after(results_wrapper)
    }

$(document).tooltip();

$(function() {
    var moveLeft = 0;
    var moveDown = 0;
    $('a.popper').hover(function(e) {
   
        var target = '#' + ($(this).attr('data-popbox'));
         
        $(target).show();
        moveLeft = $(this).outerWidth();
        moveDown = ($(target).outerHeight() / 2);
    }, function() {
        var target = '#' + ($(this).attr('data-popbox'));
        $(target).hide();
    });
 
    $('a.popper').mousemove(function(e) {
        var target = '#' + ($(this).attr('data-popbox'));
         
        leftD = e.pageX + parseInt(moveLeft);
        maxRight = leftD + $(target).outerWidth();
        windowLeft = $(window).width() - 40;
        windowRight = 0;
        maxLeft = e.pageX - (parseInt(moveLeft) + $(target).outerWidth() + 20);
         
        if(maxRight > windowLeft && maxLeft > windowRight)
        {
            leftD = maxLeft;
        }
     
        topD = e.pageY - parseInt(moveDown);
        maxBottom = parseInt(e.pageY + parseInt(moveDown) + 20);
        windowBottom = parseInt(parseInt($(document).scrollTop()) + parseInt($(window).height()));
        maxTop = topD;
        windowTop = parseInt($(document).scrollTop());
        if(maxBottom > windowBottom)
        {
            topD = windowBottom - $(target).outerHeight() - 20;
        } else if(maxTop < windowTop){
            topD = windowTop + 20;
        }
     
        $(target).css('top', topD).css('left', leftD);
     
    });
 
});

function toggle(source) {
  checkboxes = document.getElementsByName('selection');
  for(var i in checkboxes)
  checkboxes[i].checked = source.checked;
}