

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

	$("#refresh-icon").addClass("icon-spin");

	$.ajax({
		url: "cgi-bin/get_connections.py"
	}).done(function (data) {
		app.connections = data;
		app.show_filtered_data();
	}).fail(function () {
		console.console.log("Petition fails...");
	}).always(function (){
		$("#refresh-icon").removeClass("icon-spin");
	});
};

app.show_filtered_data = function () {

	var filter_str, filter_data;

	filter_str = $("input#filter_input").val();

	filter_data = filter_str === "" ? app.connections :
		app.connections.filter(function (item) {
			return item.ip_origen.indexOf(filter_str) === 0;
		}
	);

	app.populate_connections(filter_data);
};

$(document).ready(app.get_connections);
