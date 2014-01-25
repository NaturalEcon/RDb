$(document).ready(function(){

	$("#form").css("display","none");
	$("#content > a").click(function(){
		$("#info > p").hide("fast");
		$("#form").show("fast");
	});

});
