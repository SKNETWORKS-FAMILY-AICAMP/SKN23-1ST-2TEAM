import streamlit.components.v1 as components

def get_gps():
    gps_html = """
    <script>
    navigator.geolocation.getCurrentPosition((pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        var data = lat + "," + lng;
        const streamlitMsg = {isStreamlitMessage: true, data: data};
        window.parent.postMessage(streamlitMsg, "*");
    });
    </script>
    """

    return components.html(gps_html, height=0)