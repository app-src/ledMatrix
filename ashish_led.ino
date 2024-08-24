#include <FastLED.h>

#define LED_PIN       27       // Pin connected to the data input of the WS2810 LEDs
#define NUM_LEDS      210     // Total number of LEDs
#define LEDS_PER_STRIP 35     // Number of LEDs per strip
#define NUM_STRIPS     6      // Number of strips
#define BRIGHTNESS     2     // Set brightness level (0-255)
#define COLOR_ORDER    GRB    // Color order for WS2810

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();  // Initialize all pixels to 'off'
  FastLED.show();
}

void loop() {
  fillColumns();
  delay(1000);  // Wait before starting the animation again
  FastLED.clear();
}

// Function to fill LEDs column by column
void fillColumns() {
  for (int row = 0; row < LEDS_PER_STRIP; row++) {
    for (int col = 0; col < NUM_STRIPS; col++) {
      int index = calculateIndex(row, col);
      leds[index] = CRGB::Red;  // Set color to red, adjust as needed
    }
    FastLED.show();
    delay(100);  // Delay between filling each column
  }
}

// Function to calculate the linear index based on zigzag pattern
int calculateIndex(int row, int col) {
  if (row % 2 == 0) {
    return row * LEDS_PER_STRIP + col;  // For even rows, left to right
  } else {
    return (row + 1) * LEDS_PER_STRIP - 1 - col;  // For odd rows, right to left
  }
}
