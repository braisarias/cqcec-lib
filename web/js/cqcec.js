

var app = {};

app.get_info_from_connection = function (a, ip_origen, ip_dest){
	$("#connections #" + a + " .more").slideToggle("slow");

	$.ajax({
		url: "cgi-bin/get_connection_details.py",
		data: {ip_origen: ip_origen, ip_destino: ip_dest}
	}).done(function (data) {
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

app.get_connections = function (direct) {

	$("#refresh-icon").addClass("icon-spin");

	$.ajax({
		url: "cgi-bin/get_connections.py",
		data: {direction: direct}
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

app.show_historic = function () {
	var ctx;

	var html_body = Handlebars.templates.historic({});
	$("#web_body").html(html_body);

	ctx = document.getElementById("historic_chart").getContext("2d");

	$.ajax({
		url: "cgi-bin/get-historic.py"
	}).done(function (data) {

		console.log(data);

		var x = Math.floor(data.length / 6);

		new Chart(ctx).Line({
			labels: data.map(function (item,index) {
				var dt = new Date(0);
				if (index%x == 0){
					dt.setUTCSeconds(item.time);
					return dt.getHours().toString() + ":" + dt.getMinutes().toString();
				} else {
					return "";
				}
			}),
			datasets: [{
				fillColor : "rgba(220,220,220,0.5)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
				data : data.map(function (item) {return item.conns;})
			}]
		},
		{
			scaleShowLabels: true,
			scaleOverlay:true
		});
	});
};


app.enable_historic_tab = function () {
	$("ul.nav-pills li").removeClass("active");
	$("li#historic_tab").addClass("active");
	app.show_historic();
}

app.enable_output_tab = function () {
	$("ul.nav-pills li").removeClass("active");
	$("li#output_tab").addClass("active");
	app.get_connections("Outgoing");
}

app.enable_input_tab = function () {
	$("ul.nav-pills li").removeClass("active");
	$("li#input_tab").addClass("active");
	app.get_connections("Incoming");
}

$(document).ready(app.get_connections);
