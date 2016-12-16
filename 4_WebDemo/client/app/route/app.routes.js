"use strict";
var router_1 = require('@angular/router');
var common_1 = require("@angular/common");
var routes = [];
exports.appRouterProviders = [
    router_1.provideRouter(routes),
    { provide: common_1.LocationStrategy, useClass: common_1.HashLocationStrategy }
];
//# sourceMappingURL=app.routes.js.map