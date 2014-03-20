(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['connectiondetails'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n				<dt>"
    + escapeExpression(((stack1 = ((stack1 = data),stack1 == null || stack1 === false ? stack1 : stack1.key)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</dt>\n				<dd>"
    + escapeExpression((typeof depth0 === functionType ? depth0.apply(depth0) : depth0))
    + "</dd>\n			";
  return buffer;
  }

  buffer += "<div class=\"ip-info-box row clearfix\">\n	<div class=\"column-ip-info col-md-6 column ip-info-left\">\n		<h4>IP Orixe</h4>\n		<dl class=\"dl-horizontal\">\n			";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.origen), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n		</dl>\n	</div>\n	<div class=\"column-ip-info col-md-6 column ip-info-right\">\n		<h4>IP Destino</h4>\n		<dl class=\"dl-horizontal \">\n			";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.destino), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n		</dl>\n	</div>\n</div>";
  return buffer;
  });
})();