$('.chonglu1').on('click', function (event) {
    //$('#luyin1').bind('click', function (event) {
    //    var _this = $(this);
    //    _this.unbind();
    //    luyin1Callback(_this);
    //});
    stopCount1();
    var _this = $(event.target);
    $.confirm("重录将删除之前的录音", "提示", function () {
        $('#luyin1').attr('src', 'http://res.jian-hu.cn/static/img/luyin@2x.png');
        _this.parent().parent().parent().prev().html("点击开始录音，最多录60秒");
        _this.parent().parent().prev().prev().html("");
        _this.parent().html("");
    }, function () {
        //取消操作
    });
});

$('.chonglu2').on('click', function (event) {
    var _this = $(event.target);
    $.confirm("重录将删除之前的录音", "提示", function () {
        $('#luyin2').attr('src', 'http://res.jian-hu.cn/static/img/luyin@2x.png');
        _this.parent().parent().parent().prev().html("点击开始录音，最多录60秒");
        _this.parent().parent().prev().prev().html("");
        _this.parent().html("");
    }, function () {
        //取消操作
    });
});


$('#luyin1').bind('click', function (event) {
    var _this = $(this);
    _this.unbind();
    luyin1Callback(_this);
});

function luyin1Callback(_this) {
    //1.更新点击录音图片，实现360度旋转
    _this.attr('src', 'http://res.jian-hu.cn/static/img/luyinzhong@3x.gif');
    //2.更新点击开始录音文本
    timedCount1();
    _this.parent().parent().parent().prev().html('已录 <font style="color: #ff9600;" id="count1">0</font> 秒');
    //3.更新将左边空白部分替换成暂停图片按钮
    var start = '<div class="jian-luyin-start-img" id="jian-luyin-stop"><img src="http://res.jian-hu.cn/static/img/stop@2x.png" class="jian-luyin-stop"></div>';
    _this.parent().parent().prev().html(start);
    //右边的重录按钮消失
    $('.chonglu1').html('');

}

//第二个
$('#luyin2').on('click', function (event) {
    var _this = $(this);
    //1.更新点击录音图片，实现360度旋转
    _this.attr('src', 'http://res.jian-hu.cn/static/img/luyinzhong@3x.gif');
    //2.更新点击开始录音文本
    timedCount2();
    _this.parent().parent().parent().prev().html('已录 <font style="color: #ff9600;" id="count2">0</font> 秒');

    //3.更新将左边空白部分替换成暂停图片按钮
    var start = '<div class="jian-luyin-start-img" id="jian-luyin-stop"><img src="http://res.jian-hu.cn/static/img/stop@2x.png" class="jian-luyin-stop" ></div>';
    _this.parent().parent().prev().html(start);
});


//暂停录音
$('#jian-luyin-start1').on('click', '#jian-luyin-stop', function (event) {
    $('#luyin1').bind('click', function (event) {
        var _this = $(this);
        _this.unbind();
        luyin1Callback(_this);
    });
    stopCount1();
    var _this = $(this).children('.jian-luyin-stop');
    var img_dom = _this.parent().parent().next().find('.jian-luyin-img');
    img_dom.attr('src', 'http://res.jian-hu.cn/static/img/bofang@2x.png');
    var chonglu = _this.parent().parent().next().next();
    chonglu.find('.chonglu1').html('<div class="jian-luyin-2">重录</div>');

    _this.parent().parent().html('');

});

$('#jian-luyin-start2').on('click', '#jian-luyin-stop', function (event) {
    stopCount2();
    var _this = $(this).children('.jian-luyin-stop');
    var img_dom = _this.parent().parent().next().find('.jian-luyin-img');
    img_dom.attr('src', 'http://res.jian-hu.cn/static/img/bofang@2x.png');
    var chonglu = _this.parent().parent().next().next();
    console.log(chonglu);
    chonglu.find('.chonglu2').html('<div class="jian-luyin-2">重录</div>');
    _this.parent().parent().html('');
    // console.log(img_dom);
    // alert('stop');
});

$('.jian-fasong-btn').on('click', function (event) {
    // $.confirm("重录将删除之前的录音", "提示", function() {
    location.href = "/";
    // }, function() {
    //   //取消操作
    // });
});


var second1 = 0
var timer1;
function timedCount1() {
    $('#count1').text(second1);
    second1 = second1 + 1;
    timer1 = setTimeout("timedCount1()", 1000)
}

function stopCount1() {
    $('#count1').text(second1);
    clearTimeout(timer1);
    second1 = 0;
}

var second2 = 0;
var timer2;
function timedCount2() {
    $('#count1').text(second2);
    second2 = second1 + 1;
    timer2 = setTimeout("timedCount2()", 1000);
}

function stopCount2() {
    $('#count1').text(second2);
    clearTimeout(timer2);
    second2 = 0;
}
