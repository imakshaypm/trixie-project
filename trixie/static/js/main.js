/*// Query DOM Elements
const path = document.querySelector('.infinity');
const circle = document.querySelector('.circle');

// Create an object that gsap can animate
const val = { distance: 0 };
// Create a tween
gsap.to(val, {
    // Animate from distance 0 to the total distance
    distance: path.getTotalLength(),
    // Loop the animation
    repeat: -1,
    // Make the animation lasts 5 seconds
    duration: 20,
    // Function call on each frame of the animation
    onUpdate: () => {
        // Query a point at the new distance value
        const point = path.getPointAtLength(val.distance);
        // Update the circle coordinates
        circle.setAttribute('cx', point.x);
        circle.setAttribute('cy', point.y);
    }
});*/

function positionCar() {
    var scrollY = window.scrollY || window.pageYOffset;
    var maxScrollY = document.documentElement.scrollHeight - window.innerHeight;
    var path = document.getElementById("path1");
    // Calculate distance along the path the car should be for the current scroll amount
    var pathLen = path.getTotalLength();
    var dist = pathLen * scrollY / maxScrollY;
    var pos = path.getPointAtLength(dist);
    // Calculate position a little ahead of the car (or behind if we are at the end), so we can calculate car angle
    if (dist + 1 <= pathLen) {
        var posAhead = path.getPointAtLength(dist + 1);
        var angle = Math.atan2(posAhead.y - pos.y, posAhead.x - pos.x);
    } else {
        var posBehind = path.getPointAtLength(dist - 1);
        var angle = Math.atan2(pos.y - posBehind.y, pos.x - posBehind.x);
    }
    // Position the car at "pos" totated by "angle"
    var car = document.getElementById("cir");
    car.setAttribute("transform", "translate(" + pos.x + "," + pos.y + ") rotate(" + rad2deg(angle) + ")");
}

function rad2deg(rad) {
    return 180 * rad / Math.PI;
}

// Reposition car whenever there is a scroll event
window.addEventListener("scroll", positionCar);

// Position the car initially
positionCar();