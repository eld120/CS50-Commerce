
const menu = document.querySelector('#menu');

menu.addEventListener('click', () => {
    if (menu.classList.contains('open')) {
        menu.classList.remove('open');
        console.log('is open');
    }
    else {
        menu.classList.add('open');
        console.log('is closed');
    }
});








// from lincoln loop website
// !(function (t) {
//   var e = {};
//   function n(i) {
//     if (e[i]) return e[i].exports;
//     var o = (e[i] = { i: i, l: !1, exports: {} });
//     return t[i].call(o.exports, o, o.exports, n), (o.l = !0), o.exports;
//   }
//   (n.m = t),
//     (n.c = e),
//     (n.d = function (t, e, i) {
//       n.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: i });
//     }),
//     (n.r = function (t) {
//       "undefined" != typeof Symbol &&
//         Symbol.toStringTag &&
//         Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
//         Object.defineProperty(t, "__esModule", { value: !0 });
//     }),
//     (n.t = function (t, e) {
//       if ((1 & e && (t = n(t)), 8 & e)) return t;
//       if (4 & e && "object" == typeof t && t && t.__esModule) return t;
//       var i = Object.create(null);
//       if (
//         (n.r(i),
//         Object.defineProperty(i, "default", { enumerable: !0, value: t }),
//         2 & e && "string" != typeof t)
//       )
//         for (var o in t)
//           n.d(
//             i,
//             o,
//             function (e) {
//               return t[e];
//             }.bind(null, o)
//           );
//       return i;
//     }),
//     (n.n = function (t) {
//       var e =
//         t && t.__esModule
//           ? function () {
//               return t.default;
//             }
//           : function () {
//               return t;
//             };
//       return n.d(e, "a", e), e;
//     }),
//     (n.o = function (t, e) {
//       return Object.prototype.hasOwnProperty.call(t, e);
//     }),
//     (n.p = ""),
//     n((n.s = 3));
// })([
//   function (t, e) {
//     function n(t, e, n) {
//       var i, o, s, r, l;
//       function c() {
//         var u = Date.now() - r;
//         u < e && u >= 0
//           ? (i = setTimeout(c, e - u))
//           : ((i = null), n || ((l = t.apply(s, o)), (s = o = null)));
//       }
//       null == e && (e = 100);
//       var u = function () {
//         (s = this), (o = arguments), (r = Date.now());
//         var u = n && !i;
//         return (
//           i || (i = setTimeout(c, e)),
//           u && ((l = t.apply(s, o)), (s = o = null)),
//           l
//         );
//       };
//       return (
//         (u.clear = function () {
//           i && (clearTimeout(i), (i = null));
//         }),
//         (u.flush = function () {
//           i &&
//             ((l = t.apply(s, o)), (s = o = null), clearTimeout(i), (i = null));
//         }),
//         u
//       );
//     }
//     (n.debounce = n), (t.exports = n);
//   },
//   function (t, e, n) {
//     var i, o, s;
//     /*!
//      * headroom.js v0.7.0 - Give your page some headroom. Hide your header until you need it
//      * Copyright (c) 2015 Nick Williams - http://wicky.nillia.ms/headroom.js
//      * License: MIT
//      */ !(function (n, r) {
//       "use strict";
//       (o = []),
//         void 0 ===
//           (s =
//             "function" ==
//             typeof (i = function () {
//               var t = {
//                 bind: !!function () {}.bind,
//                 classList: "classList" in document.documentElement,
//                 rAF: !!(
//                   window.requestAnimationFrame ||
//                   window.webkitRequestAnimationFrame ||
//                   window.mozRequestAnimationFrame
//                 ),
//               };
//               function e(t) {
//                 (this.callback = t), (this.ticking = !1);
//               }
//               function n(t) {
//                 return (
//                   t &&
//                   "undefined" != typeof window &&
//                   (t === window || t.nodeType)
//                 );
//               }
//               function i(t, o) {
//                 var s;
//                 (o = (function t(e) {
//                   if (arguments.length <= 0)
//                     throw new Error("Missing arguments in extend function");
//                   var i,
//                     o,
//                     s = e || {};
//                   for (o = 1; o < arguments.length; o++) {
//                     var r = arguments[o] || {};
//                     for (i in r)
//                       "object" != typeof s[i] || n(s[i])
//                         ? (s[i] = s[i] || r[i])
//                         : (s[i] = t(s[i], r[i]));
//                   }
//                   return s;
//                 })(o, i.options)),
//                   (this.lastKnownScrollY = 0),
//                   (this.elem = t),
//                   (this.debouncer = new e(this.update.bind(this))),
//                   (this.tolerance =
//                     (s = o.tolerance) === Object(s) ? s : { down: s, up: s }),
//                   (this.classes = o.classes),
//                   (this.offset = o.offset),
//                   (this.scroller = o.scroller),
//                   (this.initialised = !1),
//                   (this.onPin = o.onPin),
//                   (this.onUnpin = o.onUnpin),
//                   (this.onTop = o.onTop),
//                   (this.onNotTop = o.onNotTop);
//               }
//               return (
//                 (window.requestAnimationFrame =
//                   window.requestAnimationFrame ||
//                   window.webkitRequestAnimationFrame ||
//                   window.mozRequestAnimationFrame),
//                 (e.prototype = {
//                   constructor: e,
//                   update: function () {
//                     this.callback && this.callback(), (this.ticking = !1);
//                   },
//                   requestTick: function () {
//                     this.ticking ||
//                       (requestAnimationFrame(
//                         this.rafCallback ||
//                           (this.rafCallback = this.update.bind(this))
//                       ),
//                       (this.ticking = !0));
//                   },
//                   handleEvent: function () {
//                     this.requestTick();
//                   },
//                 }),
//                 (i.prototype = {
//                   constructor: i,
//                   init: function () {
//                     if (i.cutsTheMustard)
//                       return (
//                         this.elem.classList.add(this.classes.initial),
//                         setTimeout(this.attachEvent.bind(this), 100),
//                         this
//                       );
//                   },
//                   destroy: function () {
//                     var t = this.classes;
//                     (this.initialised = !1),
//                       this.elem.classList.remove(
//                         t.unpinned,
//                         t.pinned,
//                         t.top,
//                         t.initial
//                       ),
//                       this.scroller.removeEventListener(
//                         "scroll",
//                         this.debouncer,
//                         !1
//                       );
//                   },
//                   attachEvent: function () {
//                     this.initialised ||
//                       ((this.lastKnownScrollY = this.getScrollY()),
//                       (this.initialised = !0),
//                       this.scroller.addEventListener(
//                         "scroll",
//                         this.debouncer,
//                         !1
//                       ),
//                       this.debouncer.handleEvent());
//                   },
//                   unpin: function () {
//                     var t = this.elem.classList,
//                       e = this.classes;
//                     (!t.contains(e.pinned) && t.contains(e.unpinned)) ||
//                       (t.add(e.unpinned),
//                       t.remove(e.pinned),
//                       this.onUnpin && this.onUnpin.call(this));
//                   },
//                   pin: function () {
//                     var t = this.elem.classList,
//                       e = this.classes;
//                     t.contains(e.unpinned) &&
//                       (t.remove(e.unpinned),
//                       t.add(e.pinned),
//                       this.onPin && this.onPin.call(this));
//                   },
//                   top: function () {
//                     var t = this.elem.classList,
//                       e = this.classes;
//                     t.contains(e.top) ||
//                       (t.add(e.top),
//                       t.remove(e.notTop),
//                       this.onTop && this.onTop.call(this));
//                   },
//                   notTop: function () {
//                     var t = this.elem.classList,
//                       e = this.classes;
//                     t.contains(e.notTop) ||
//                       (t.add(e.notTop),
//                       t.remove(e.top),
//                       this.onNotTop && this.onNotTop.call(this));
//                   },
//                   getScrollY: function () {
//                     return void 0 !== this.scroller.pageYOffset
//                       ? this.scroller.pageYOffset
//                       : void 0 !== this.scroller.scrollTop
//                       ? this.scroller.scrollTop
//                       : (
//                           document.documentElement ||
//                           document.body.parentNode ||
//                           document.body
//                         ).scrollTop;
//                   },
//                   getViewportHeight: function () {
//                     return (
//                       window.innerHeight ||
//                       document.documentElement.clientHeight ||
//                       document.body.clientHeight
//                     );
//                   },
//                   getDocumentHeight: function () {
//                     var t = document.body,
//                       e = document.documentElement;
//                     return Math.max(
//                       t.scrollHeight,
//                       e.scrollHeight,
//                       t.offsetHeight,
//                       e.offsetHeight,
//                       t.clientHeight,
//                       e.clientHeight
//                     );
//                   },
//                   getElementHeight: function (t) {
//                     return Math.max(
//                       t.scrollHeight,
//                       t.offsetHeight,
//                       t.clientHeight
//                     );
//                   },
//                   getScrollerHeight: function () {
//                     return this.scroller === window ||
//                       this.scroller === document.body
//                       ? this.getDocumentHeight()
//                       : this.getElementHeight(this.scroller);
//                   },
//                   isOutOfBounds: function (t) {
//                     var e = t < 0,
//                       n =
//                         t + this.getViewportHeight() > this.getScrollerHeight();
//                     return e || n;
//                   },
//                   toleranceExceeded: function (t, e) {
//                     return (
//                       Math.abs(t - this.lastKnownScrollY) >= this.tolerance[e]
//                     );
//                   },
//                   shouldUnpin: function (t, e) {
//                     var n = t > this.lastKnownScrollY,
//                       i = t >= this.offset;
//                     return n && i && e;
//                   },
//                   shouldPin: function (t, e) {
//                     var n = t < this.lastKnownScrollY,
//                       i = t <= this.offset;
//                     return (n && e) || i;
//                   },
//                   update: function () {
//                     var t = this.getScrollY(),
//                       e = t > this.lastKnownScrollY ? "down" : "up",
//                       n = this.toleranceExceeded(t, e);
//                     this.isOutOfBounds(t) ||
//                       (t <= this.offset ? this.top() : this.notTop(),
//                       this.shouldUnpin(t, n)
//                         ? this.unpin()
//                         : this.shouldPin(t, n) && this.pin(),
//                       (this.lastKnownScrollY = t));
//                   },
//                 }),
//                 (i.options = {
//                   tolerance: { up: 0, down: 0 },
//                   offset: 0,
//                   scroller: window,
//                   classes: {
//                     pinned: "headroom--pinned",
//                     unpinned: "headroom--unpinned",
//                     top: "headroom--top",
//                     notTop: "headroom--not-top",
//                     initial: "headroom",
//                   },
//                 }),
//                 (i.cutsTheMustard =
//                   void 0 !== t && t.rAF && t.bind && t.classList),
//                 i
//               );
//             })
//               ? i.apply(e, o)
//               : i) || (t.exports = s);
//     })();
//   },
//   ,
//   function (t, e, n) {
//     "use strict";
//     n.r(e);
//     var i = n(0),
//       o = n.n(i),
//       s = function () {
//         if (document.querySelector("body").classList.contains("homepage")) {
//           var t = document.querySelector(".hero-block"),
//             e = getComputedStyle(t);
//           return (
//             t.clientTop +
//             t.offsetHeight +
//             parseInt(e.marginTop) +
//             parseInt(e.marginBottom)
//           );
//         }
//         return 0;
//       },
//       r = n(1),
//       l = new (n.n(r).a)(document.getElementById("Site-Header"), {
//         offset: s(),
//         tolerance: 10,
//         classes: {
//           initial: "animated",
//           pinned: "is-pinned",
//           unpinned: "is-unpinned",
//           top: "is-top",
//           notTop: "is-not-top",
//         },
//       }).init(),
//       c = function () {
//         l
//           ? (l.offset = s())
//           : ((document.querySelector("#Site-Header").style.visibility =
//               "visible"),
//             (document.querySelector(".PrimaryNav").style.display = "block"));
//       },
//       u = "animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd",
//       a = { "md-display": 720, "max-display": 1280 },
//       d = function (t) {
//         var e = document.querySelector(".hero-block"),
//           n = document.querySelector("#Site-Header");
//         if (t) {
//           var i = "".concat(e.offsetHeight - t, "px");
//           (e.style.height = i), (n.style.top = i);
//         } else (e.style.height = ""), (n.style.top = "");
//       },
//       h = function () {
//         d();
//         document.querySelector(".hero-block"),
//           document.querySelector("#Site-Header");
//         if (document.body.offsetWidth > a["md-display"]) {
//           var t =
//             document.querySelector(".hero-block").offsetHeight +
//             document.querySelector("#Site-Header").offsetHeight -
//             window.height;
//           t > 0 ? d(t) : d();
//         } else d();
//         c();
//       };
//     document.body.classList.contains("homepage")
//       ? (h(), window.addEventListener("resize", o()(h, 200)))
//       : c();
//     document.addEventListener("roundup-signup", function () {
//       "lincolnloop.com" !== document.location.hostname ||
//         localStorage.getItem("roundup-signup") ||
//         (localStorage.setItem("roundup-signup", 1),
//         window.ga && window.ga("send", "event", "Signup", "Django List"));
//     });
//     var p = function (t) {
//         t.currentTarget.parentElement.classList.add("has-focus");
//       },
//       f = function (t) {
//         t.currentTarget.parentElement.classList.remove("has-focus");
//       };
//     document.querySelectorAll("select").forEach(function (t) {
//       return t.addEventListener("focus", p);
//     }),
//       document.querySelectorAll("select").forEach(function (t) {
//         return t.addEventListener("blur", f);
//       }),
//       document
//         .querySelector(".SiteHeader-menuToggle")
//         .addEventListener("click", function (t) {
//           t.preventDefault(),
//             document
//               .querySelector("#Primary-Nav")
//               .classList.toggle("PrimaryNav--expanded");
//         }),
//       document.querySelector("#Primary-Nav").addEventListener(u, c),
//       window.addEventListener("resize", o()(c, 300));
//   },
// ]);
