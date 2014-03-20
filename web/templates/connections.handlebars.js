(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['connections'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n	<li id=\"conn"
    + escapeExpression(((stack1 = ((stack1 = data),stack1 == null || stack1 === false ? stack1 : stack1.index)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" class=\"well well-sm connection\" onclick=\"app.get_info_from_connection('conn"
    + escapeExpression(((stack1 = ((stack1 = data),stack1 == null || stack1 === false ? stack1 : stack1.index)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "', '"
    + escapeExpression(((stack1 = (depth0 && depth0.ip_origen)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "', '"
    + escapeExpression(((stack1 = (depth0 && depth0.ip_dest)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "')\">\n		<div class=\"brief\">\n			<span class=\"ip\">"
    + escapeExpression(((stack1 = (depth0 && depth0.ip_origen)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n			<span class=\"glyphicon glyphicon-arrow-right\"></span>\n			<span class=\"proto\">"
    + escapeExpression(((stack1 = (depth0 && depth0.proto)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n			<span class=\"glyphicon glyphicon-arrow-right\"></span>\n			<span class=\"ip\">"
    + escapeExpression(((stack1 = (depth0 && depth0.ip_dest)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\n		</div>\n		<div class=\"more\">\n			<hr>\n			<div class=\"details\">\n				<i class=\"icon-spin icon-refresh refresh-icon\"></i>\n			</div>\n		</div>\n	</li>\n	";
  return buffer;
  }

  buffer += "<ul id=\"connections\">\n	";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.connections), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</ul>";
  return buffer;
  });
})();
