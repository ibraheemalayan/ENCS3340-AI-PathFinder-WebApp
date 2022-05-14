let map;

var current_id = null;


function render(data){

    console.log("RENDERING ...");

    var styles = [
        {
            "featureType": "landscape.man_made",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f7f1df"
                }
            ]
        },
        {
            "featureType": "landscape.natural",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#d0e3b4"
                }
            ]
        },
        {
            "featureType": "landscape.natural.terrain",
            "elementType": "geometry",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi.business",
            "elementType": "all",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi.medical",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#fbd3da"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#bde6ab"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "labels",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#ffe15f"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                    "color": "#efd151"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#ffffff"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "black"
                }
            ]
        },
        {
            "featureType": "transit.station.airport",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#cfb2db"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#a2daf2"
                }
            ]
        }
    ];

    const starting_lat_lng = { lng: parseFloat(data.view_lng), lat: parseFloat(data.view_lat)  };

    map = new google.maps.Map(document.getElementById("map"), {
        center: starting_lat_lng,
        zoom: data.view_zoom,
        mapId: "47beb21b23161ed8"
    });

    for (const node of data.graph.nodes){

        const LatLng = { lng: parseFloat(node.longitude), lat: parseFloat(node.latitude)  };

        const marker = new google.maps.Marker({
            position: LatLng,
            map,
            title: node.id,
          });

          marker.addListener("click", () => {
            marker_clicked(marker.getTitle());
            console.log("MARKER CLICKED: "  + marker.getTitle() );

            // animate
            marker.setAnimation(google.maps.Animation.BOUNCE);

            setTimeout(function() {
              marker.setAnimation(null);
            }, 500);

          });


          

    }


    
}
function initMap() {

    fetch('/load_graph')
      .then(response => response.json())
      .then(data => render(data));
}

function marker_clicked(marker_name){

    const shake_animation = [
        { transform: 'translateX(0)' },
        { transform: 'translateX(5px)' },
        { transform: 'translateX(10px)' },
        { transform: 'translateX(0px)' },
        { transform: 'translateX(-10px)' },
        { transform: 'translateX(-5px)' },
        { transform: 'translateX(0)' },
      ];
      
      const shake_timing = {
        duration: 500,
        iterations: 1,
      }
      

    src_city_label =  document.getElementById("src_city");
    dest_city_label =  document.getElementById("dest_city");

    if (window.selected_nodes.length == 0){
       src_city_label.value = marker_name;
       src_city_label.animate(shake_animation, shake_timing);
       window.selected_nodes.push(marker_name);
    }
    else if (window.selected_nodes.length == 1){

        if (src_city_label.value == marker_name){
            src_city_label.value = "";
            window.selected_nodes = [];
            src_city_label.animate(shake_animation, shake_timing);
            return;
        }

        dest_city_label.value = marker_name;
        dest_city_label.animate(shake_animation, shake_timing);
        window.selected_nodes.push(marker_name);
    }else{

        if (dest_city_label.value == marker_name){
            dest_city_label.value = "";
            window.selected_nodes = [window.selected_nodes[0]];
            dest_city_label.animate(shake_animation, shake_timing);
            return;
        }

        window.selected_nodes[0] = window.selected_nodes[1]
        window.selected_nodes[1] = marker_name;

        src_city_label.value = window.selected_nodes[0];
        dest_city_label.value = window.selected_nodes[1];

        src_city_label.animate(shake_animation, shake_timing);
        dest_city_label.animate(shake_animation, shake_timing);
    }


}



function OpenPathPopUp(){
    var modal = document.getElementById("path_pop_up");
    modal.style.display = "block";
    document.getElementById("map").classList.add("blur");

    path_form = document.getElementById("path_form")

    const xhr = new XMLHttpRequest(),
        FD  = new FormData(path_form);

    // Define what happens on successful data submission
    xhr.addEventListener( 'load', function( event ) {
      alert(xhr.response)
    } );
  
    // Define what happens in case of error
    xhr.addEventListener(' error', function( event ) {
      alert( 'Oops! Something went wrong.' );
    } );
  
    // Set up our request
    xhr.open( 'POST', '/get_path' );
  
    // Send our FormData object; HTTP headers are set automatically
    xhr.send( FD );

}

function view_path_in_pop_up(response){

}

var p = document.getElementById("path_pop_up");
var close = document.getElementById("close_path");

close.onclick = function() {
  p.style.display = "none";
  document.getElementById("map").classList.remove("blur");
}

window.onclick = function(event) {
  if (event.target == p) {
    p.style.display = "none";
  }
}
