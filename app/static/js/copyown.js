(function() {
  n && "function" == typeof n && n.apply(this, arguments);
  var r = Array.prototype.slice.call(arguments);
  try {
    var i = r.map((function(e) {
      return Xb(e, t)
    }));
    return e.handleEvent ? e.handleEvent.apply(this, i) : e.apply(this, i)
  } catch (e) {
    throw Zb(), Object(Wb.b)((function(n) {
      n.addEventProcessor((function(e) {
        var n = X_.a({}, e);
        return t.mechanism && (Object(rb.b)(n, void 0, void 0), Object(rb.a)(n, t.mechanism)), n.extra = X_.a({}, n.extra, {
          arguments: Object(sb.c)(r, 3)
        }), n
      })), Object(Wb.a)(e)
    })), e
  }
})();
