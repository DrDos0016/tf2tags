$('document').ready(function() {

    $('.pageSelect').click(function (){
        $('.pageJump').toggle();
    });
    
    $('input[name=go]').click(function (){
        $('input[name=page]').each(function (){
            if ($(this).val() != "")
                page = $(this).val();
        });
        var destination = type+page+qs;
        window.location = destination;
    });
});