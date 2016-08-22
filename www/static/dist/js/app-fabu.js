

$('.weui-col-33').on('click','.jian-form-edit', function (event) {
    var _this = $(this);
    if(_this.hasClass('jian-add-skill')){
        return;
    }
    _this.next().toggle();
});


//删除技能要求
$(".weui-row").on('click', '.jian-skill-clear', function (event) {
    var _this = $(event.target);
    var skill = _this.prev();
    var curr_id = skill.attr('id');
    for (var i = parseInt(curr_id); i <= 6; i++) {
        if ($('#' + i).hasClass('jian-add-skill')) {
            for (var j = i; j <= 6; j++) {
                $('#' + j).removeClass('jian-form-edit').removeClass('jian-add-skill').html('');
            }
            $('#' + (i - 1)).addClass('jian-add-skill');
            $('#' + (i - 1)).next().remove();
        }
        if ($('#6').text().trim() !== '') {  //说明已经有6条技能了
            if (i == 6) {
                $('#6').html('<img src="http://res.jian-hu.cn/static/img/add@2x.png" height="16px">').addClass('jian-add-skill');
                $('#6').next().remove();
            } else {
                $('#' + i).html($('#' + (i + 1)).html());
                //$('#' + i).next().toggle();
            }
        } else {
            $('#' + i).html($('#' + (i + 1)).html());
        }
    }
    $('#' + curr_id).next().toggle();
});


//给动态添加的元素添加事件要使用委托
$(".weui-row").on('click', '.jian-add-skill', function (event) {
    var _this = $(event.target);
    if (_this.attr('id') === undefined) { //如果点击的是'.jian-add-skill'的子元素，也就是+这个符号
        _this = _this.parent();
    }
    ;
    if ($('.weui-col-50 .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定', 'warning');
    } else {
        myPrompt(_this);
    }
});


function myPrompt(_this) {
    $.prompt("", "限16个字符且不为空", function (_text) {
        if (!isLimit(_text, 16) || (_text.trim()) == '') {
            myPrompt(_this);
            $('.weui_dialog_title').css('color', 'red');
        }
        else {
            curr_id = parseInt(_this.attr('id'));
            _this.removeClass('jian-add-skill');
            if (curr_id <= 6) {
                $('#' + (curr_id + 1)).addClass('jian-add-skill').addClass('jian-form-edit').html(_this.html());
            }
            _this.html(_text);
            _this.after('<img src="http://res.jian-hu.cn/static/img/close@2x.png" class="jian-skill-clear">');
            $(".skill"+curr_id).val(_text);
        }
    }, function () {
        //取消操作
    });
}

$(".jian-fabu-btn").on('click', '', function (event) {
    if ($('.jian-upload-label .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定图片添加', 'warning');
        return;
    }
    if ($('.weui-col-50 .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定技能标签', 'warning');
        return;
    }
    if($("#company_name").val()==''){
        $.toptip('请先填写公司名称', 'warning');
        return;
    }
    if($("#job_title").val()==''){
        $.toptip('请先填写职位名称', 'warning');
        return;
    }
    $.confirm("确认后不可撤回哦！", "确认发送?", function () {
        $('.myform').submit();
    }, function () {
        //取消操作
    });
});


//编辑图片
$('.weui-col-33').on('click','.mimg', function (event) {
    var _this = $(this);
    if(_this.hasClass('weui_uploader_input_wrp')){
        return;
    }
   _this.next().toggle();
});


//删除图片
$(".weui-row").on('click', '.jian-img-clear', function (event) {
    var _this = $(event.target);
    var imgdiv = _this.parent();
    var curr_id = imgdiv.attr('id').substring(6, 7);
    var imgdiv7 = '';
    if ($('#imgdiv6').find('.mimg').length !== 0) {
        imgdiv7 = '<div class="weui_uploader_input_wrp" style="margin:0"><div class="weui_uploader_input"></div></div>';
    }

    for(var i = parseInt(curr_id); i<=6;i++){
        if (i==6) {
            $('#imgdiv'+i).html(imgdiv7);
        }
        else{
            $('#imgdiv'+i).html($('#imgdiv'+(i+1)).html());
        }
    }
    for(var i = 1; i<=6;i++){
        if($('#imgdiv'+i).children().length==0){
            console.log(i);
            $('#imgdiv'+i).css('height','0');
        }else{
            formatUpload("imgdiv6");
        }
    }
});


//添加图片


function addImg(_this, img_src) {
    var imgdiv = _this.parent().parent();
    var dom = '<img src="' + img_src + '" class="mimg" ><img src="http://res.jian-hu.cn/static/img/close@2x.png" class="jian-img-clear">'
    imgdiv.html(dom);
    var curr_id = imgdiv.attr('id');
    formatUpload(curr_id);//自动缩放图片
    if (curr_id !== 'imgdiv6') { //替换下一个图片div的样式
        id_num = parseInt(curr_id.substring(6, 7));
        var next_id = "imgdiv" + (id_num + 1);
        $("#" + next_id).html('<div class="weui_uploader_input_wrp" style="margin:0"><div class="weui_uploader_input"></div></div>');
        formatUpload(next_id);//自动缩放图片
    }
}

$("#city-picker").cityPicker({
    showDistrict: true
});


function formatUpload(id) {
    var width = $('#' + id).width();
    $('#' + id).height(width);

    $('.weui_uploader_input_wrp').height(width - 2);//去除两个border的宽度2px
    $('.weui_uploader_input_wrp').width(width - 2);

    $('#' + id).each(function (index, el) {
        setImgAutoSize($(this).find('.mimg'));
    });
}
formatUpload("imgdiv1");

function isLimit(val, max) {
    var returnValue = '';
    var byteValLen = 0;
    for (var i = 0; i < val.length; i++) {
        if (val[i].match(/[^\x00-\xff]/ig) != null)
            byteValLen += 2;
        else
            byteValLen += 1;
    }
    if (byteValLen > max) {
        return false;
    } else {
        return true;
    }
}

//传入的img自动等比例缩放
function setImgAutoSize(img) {
    $("<img/>").attr("src", img.attr("src")).load(function () {
        var realWidth = this.width;
        var realHeight = this.height;
        if (realHeight > realWidth) {
            img.css('width', '100%');
        } else {
            img.css('height', '100%');
            img.css('width', 'auto');
        }
    });
}