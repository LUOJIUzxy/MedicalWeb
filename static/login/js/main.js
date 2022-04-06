function getAuthcode(){
    $("getAuthcode").click(function(){
    $.get("/yanzheng/", function(result){
        $("getAuthcode").val("正在获取。。。");
        });
    });
}

getAuthcode();