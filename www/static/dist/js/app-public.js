/**
 * Created by yang on 2016/8/23.
 */

$(function () {
    $('#closebt').click(function () {
        $('#jian-modal').hide();
        $('#jian-cover').hide();
    });
    $('#jian-cover').click(function () {
        $('#jian-modal').hide();
        $('#jian-cover').hide();
    });

});
function openModal(img_src, name, title, company, city, info) {
    $('#modal_user_img').attr('src', img_src);
    $('#name').text(name);
    $('#modal_user_title').text(title);
    $('#modal_user_company').text(company);
    $('#modal_user_city').text(city);
    $('#info').text(info);

    $('#jian-modal').center();
    $('#jian-cover').show();
    $('#jian-modal').fadeIn(100, "linear");
}


function openPostJobSuccessModal(src,title,info){
    $('#jian-modal-portrait').css({'margin': '-10px auto', 'width': '60px', 'height': '60px'});
    $('#jian-modal-portrait img').attr('src',src);
    $('#user_profile').hide();
    $('#name').text(title).css('color', '#ff9600').css("margin-top", '14px');
    $('#info').text(info).css('margin-top','18px');

    $('#jian-modal').center();
    $('#jian-cover').show();
    $('#jian-modal').fadeIn(100, "linear");
}

jQuery.fn.center = function (loaded) {
    var obj = this;
    body_width = parseInt($(window).width());
    body_height = parseInt($(window).height());
    block_width = parseInt(obj.width());
    block_height = parseInt(obj.height());

    left_position = parseInt((body_width / 2) - (block_width / 2) + $(window).scrollLeft());
    if (body_width < block_width) {
        left_position = 0 + $(window).scrollLeft();
    }

    top_position = parseInt((body_height / 2) - (block_height / 2) + $(window).scrollTop());
    if (body_height < block_height) {
        top_position = 0 + $(window).scrollTop();
    }
    ;

    if (!loaded) {

        obj.css({
            'position': 'absolute'
        });
        obj.css({
            'top': ($(window).height() - $(obj).height()) * 0.48,
            'left': left_position
        });
        $(window).bind('resize', function () {
            obj.center(!loaded);
        });
        $(window).bind('scroll', function () {
            obj.center(!loaded);
        });

    } else {
        obj.stop();
        obj.css({
            'position': 'absolute'
        });
        obj.animate({
            'top': top_position
        }, 100, 'linear');
    }
}