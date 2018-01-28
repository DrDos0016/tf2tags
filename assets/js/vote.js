$(document).ready(function () {
    $('img[name=critButton]').click(function () {
        vote($(this).data("item"), 1)
    });
    
    $('img[name=missButton]').click(function () {
        vote($(this).data("item"), -1)
    });
});

function vote(item, vote)
{
    $('#vote'+item).html("Voting...");
    ajax_url = '/ajax/vote/'+item+'/'+vote;
    $.ajax({
        url: ajax_url,
        success: function(data) {
            if (vote == -1)
                $('#vote'+item).css('color', '#F00');
            else
                $('#vote'+item).css('color', '#0F0');
            $('#vote'+item).html(data);
        }
    });
    
}