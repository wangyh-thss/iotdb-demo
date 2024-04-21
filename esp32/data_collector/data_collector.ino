int led_pin = 2;
int input_pin = 33;

int signal_1 = 0;
int signal_2 = 0;
int signal_3 = 0;

bool receiving_signal = false;
int signal[10];

bool check_signal(int signal, int expected)
{
    return signal <= expected + 2 && signal >= expected - 2;
}

void read_ball_color()
{
    signal_1 = pulseIn(input_pin, HIGH, 1000);
    signal_2 = pulseIn(input_pin, HIGH, 1000);

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
        signal_1 = pulseIn(input_pin, HIGH, 1000000);
        if (check_signal(signal_1, 27))
        {
            signal_2 = pulseIn(input_pin, HIGH, 1000);
            signal_3 = pulseIn(input_pin, HIGH, 1000);
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
    digitalWrite(led_pin, HIGH);
    delay(500);
    digitalWrite(led_pin, LOW);
}

void led_show_white()
{
    digitalWrite(led_pin, HIGH);
    delay(200);
    digitalWrite(led_pin, LOW);
    delay(100);
    digitalWrite(led_pin, HIGH);
    delay(200);
    digitalWrite(led_pin, LOW);
}

void setup()
{
    Serial.begin(115200);
    pinMode(led_pin, OUTPUT);
    pinMode(input_pin, INPUT);
}

void loop()
{
    signal_1 = pulseIn(input_pin, HIGH, 1000);
    if (check_signal(signal_1, 27))
    {
        read_ball_color();
    }
}
