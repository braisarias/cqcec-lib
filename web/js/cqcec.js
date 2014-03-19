

var app = {};

app.get_info_from_connection = function (a, ip_origen, ip_dest){
	$("#connections #" + a + " .more").slideToggle("slow");

	$.ajax({
		url: "cgi-bin/get_connection_details.py",
		data: {ip_origen: ip_origen, ip_destino: ip_dest}
	}).done(function (data) {
		console.log(data);
		var html_body = Handlebars.templates.connectiondetails(data);
		$("#connections #" + a + " .details").html(html_body);
	}).fail(function() {
		console.log("Petition fails...");
	});
};


app.populate_connections = function (connections) {
	var html_body = Handlebars.templates.connections({"connections":connections});
	$("#web_body").html(html_body);
};

app.get_connections = function () {

	$(".nav i.refresh-icon").addClass("icon-spin");

	console.log("hola!!!");

	$.ajax({
		url: "cgi-bin/get_connections.py"
	}).done(function (data) {
		console.log(data);
		app.populate_connections(data);
	}).fail(function () {
		console.console.log("Petition fails...");
	}).always(function (){
		$(".nav .refresh-icon").removeClass("icon-spin");
	});
};


$(document).ready(app.get_connections)