#version 410
#define VERTEX_IS_LATLON 0
#define VERTEX_IS_METERS 1
#define VERTEX_IS_SCREEN 2
#define REARTH_INV 1.56961231e-7

// Uniform block of global data
layout (std140) uniform global_data {
int wrap_dir;           // Wrap-around direction
float wrap_lon;         // Wrap-around longitude
float panlat;           // Map panning coordinates [deg]
float panlon;           // Map panning coordinates [deg]
float zoom;             // Screen zoom factor [-]
int screen_width;       // Screen width in pixels
int screen_height;      // Screen height in pixels
int vertex_scale_type;  // Vertex scale type
float screen_pixel_ratio; // > 1 for high-DPI screens
};

// Inputs
layout (location = 0) in vec2 vertex;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in float lat;
layout (location = 3) in float lon;
layout (location = 4) in float orientation;
layout (location = 5) in vec4 color;
layout (location = 6) in float scale;

// Outputs
flat out vec2 startPos_fs;
out vec2 vertPos_fs;
out vec4 color_fs;


void main()
{
	vec2 vAR = vec2(1.0, float(screen_width) / float(screen_height));
	vec2 flat_earth = vec2(cos(radians(panlat)), 1.0);
	float rot = radians(orientation);
    mat2 mrot = mat2(cos(rot), -sin(rot), sin(rot), cos(rot));

	// Vertex position and rotation calculations
	vec2 position = vec2(lon, lat);
	if (wrap_dir < 0 && position.x > wrap_lon) {
		position.x -= 360.0;
	} else if (wrap_dir > 0 && position.x < wrap_lon) {
		position.x += 360.0;
	}
	position -= vec2(panlon, panlat);

	vec4 pos;

	// Select vertex scale type
	switch (vertex_scale_type) {

		// Vertex coordinates are screen pixels, so correct for screen size
		case VERTEX_IS_SCREEN:
			vec2 vertex_out = scale * mrot * vertex;
			vertex_out = vec2(2.0 * vertex_out.x / float(screen_width), 2.0 * vertex_out.y / float(screen_height));
			pos = vec4(vAR * zoom * flat_earth * position + vertex_out, 0.0, 1.0);

			gl_Position = pos;
			vertPos_fs = pos.xy / pos.w;
			startPos_fs = vertPos_fs;

			break;

		// Vertex coordinates in meters use a right-handed coordinate system, where the positive x-axis points to the north
		// The elements in each vertex therefore need to be flipped
		case VERTEX_IS_METERS:
			pos = vec4(vAR * zoom * (flat_earth * position + scale * mrot * (degrees(vertex.yx * REARTH_INV))), 0.0, 1.0);

			gl_Position = pos;
			vertPos_fs = pos.xy / pos.w;
			startPos_fs = vertPos_fs;

			break;

		// Lat/lon vertex coordinates are flipped: lat is index 0, but screen y-axis, and lon is index 1, but screen x-axis
		case VERTEX_IS_LATLON:
		default:
			pos = vec4(vAR * flat_earth * zoom * (position + vertex.yx), 0.0, 1.0);

			gl_Position = pos;
			vertPos_fs = pos.xy / pos.w;
			startPos_fs = vertPos_fs;

			break;
	}

	// Colour
	color_fs = color;

}
