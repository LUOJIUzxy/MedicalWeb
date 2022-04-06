function getAuthcode(){
    $("getAuthcode").click(function(){
    $.get("/register/", function(result){
        $("getAuthcode").val("正在获取...");
        });
    });
}

getAuthcode();