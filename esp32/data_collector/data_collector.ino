#include <DHT.h>

#define LED_PIN 2

void blink(int duration_ms)
{
    digitalWrite(LED_PIN, HIGH);
    delay(duration_ms);
    digitalWrite(LED_PIN, LOW);
}

/*** START: Ball color detection ***/
#define COLOR_SENSOR_PIN 33

int signal_1 = 0;
int signal_2 = 0;
int signal_3 = 0;
bool receiving_signal = false;

bool check_signal(int signal, int expected)
{
    return signal <= expected + 2 && signal >= expected - 2;
}

void read_ball_color()
{
    signal_1 = pulseIn(COLOR_SENSOR_PIN, HIGH, 1000);
    signal_2 = pulseIn(COLOR_SENSOR_PIN, HIGH, 1000);

    if (!check_signal(signal_1, 54))
    {
        return;
    }

    bool is_blue_ball;
    if (check_signal(signal_2, 27))
    {
        is_blue_ball = true;
    }
    else if (check_signal(signal_2, 81))
    {
        is_blue_ball = false;
    }
    else
    {
        return;
    }

    for (int i = 0; i <= 5; i++)
    {
        signal_1 = pulseIn(COLOR_SENSOR_PIN, HIGH, 1000000);
        if (check_signal(signal_1, 27))
        {
            signal_2 = pulseIn(COLOR_SENSOR_PIN, HIGH, 1000);
            signal_3 = pulseIn(COLOR_SENSOR_PIN, HIGH, 1000);
            if (check_signal(signal_2, 54) && signal_3 == 0)
            {
                if (is_blue_ball)
                {
                    Serial.println("BALL_COLOR|1");
                    led_show_blue();
                }
                else
                {
                    Serial.println("BALL_COLOR|2");
                    led_show_white();
                }
            }
            return;
        }
    }
}

void led_show_blue()
{
    blink(500);
}

void led_show_white()
{
    blink(200);
    delay(100);
    blink(200);
}

void detectBallColor(void *params)
{
    pinMode(COLOR_SENSOR_PIN, INPUT);
    while (1)
    {
        signal_1 = pulseIn(COLOR_SENSOR_PIN, HIGH, 10000);
        if (check_signal(signal_1, 27))
        {
            read_ball_color();
        }
    }
}
/*** END: Ball color detection ***/

/*** START: Temperature and humidity ***/
#define DHT_PIN 4
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void readTemperatureAndHumidity(void *params)
{
    while (1)
    {
        float temperature = dht.readTemperature();
        float humidity = dht.readHumidity();
        float heat_index = dht.computeHeatIndex(temperature, humidity);
        Serial.println("TEMPERATURE|" + String(temperature));
        Serial.println("HUMIDITY|" + String(humidity));
        Serial.println("HEAT_INDEX|" + String(heat_index));
        blink(1000);
        delay(10000);
    }
}
/*** END: Temperature and humidity ***/

void setup()
{
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    dht.begin();

    xTaskCreate(detectBallColor, "detectBallColor", 1024, NULL, 1, NULL);
    xTaskCreate(readTemperatureAndHumidity, "readTemperatureAndHumidity", 1024, NULL, 1, NULL);
}

void loop()
{
}
