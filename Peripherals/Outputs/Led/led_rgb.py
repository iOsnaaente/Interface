from queue import Queue
import threading
import time

from Outputs.Led.led_control import LED


class RGB:
    red_led: LED 
    green_led: LED 
    blue_led: LED 

    debug: bool 

    def __init__( self, red_gpio, green_gpio, blue_gpio, allow_warnings = False, debug = False ) -> None:
        self.red_led = LED("Red LED", red_gpio, False, allow_warnings, debug)
        self.green_led = LED("Green LED", green_gpio, False, allow_warnings, debug)
        self.blue_led = LED("Blue LED", blue_gpio, False, allow_warnings, debug)
        self.red_led.set_pwm()
        self.green_led.set_pwm()
        self.blue_led.set_pwm()
        # Atributo de thread para fade e pisca 
        self._thread = None  
        # Sinalizador para indicar o encerramento das threads
        self._stop_thread = False  
        # Fila para controle de fade
        self._rgb_queue = Queue()

        # Inicie uma thread para atualizar a cor a partir da fila
        update_thread = threading.Thread( target = self.update_color_from_queue )
        update_thread.start()
    
    # Defina a cor controlando cada LED separadamente
    def set_color(self, color: list[int, int, int] ) -> None:
        red, green, blue = color 
        self.red_led.set_duty(red)
        self.green_led.set_duty(green)
        self.blue_led.set_duty(blue)
    
    # Acende o led com uma cor específica 
    def color( self, color: list[int] ) -> None:
        if self._thread is not None:
            self.stop_thread()
        elif self._thread.is_alive():
            self.stop_thread()
        self.set_color( color ) 

    # Para as threads 
    def stop_thread(self) -> None:
        try:
            self._stop_thread = True 
            self._thread.join()
        except:
            pass 
        finally:
            self._stop_thread = False

    # Thread para fazer o efeito de fade no LED RGB
    def _fade_thread( self, start_intensity: list, end_intensity: list, duration_ms: int ) -> None:
        while not self._stop_thread:
            start_time = time.time()*100 
            elapsed_time = 0
            while elapsed_time < duration_ms and not self._stop_thread:
                progress = min( 1, elapsed_time / duration_ms )
                current_intensity = [
                    int(start + (end - start) * progress)
                    for start, end in zip(start_intensity, end_intensity)
                ]
                self._rgb_queue.put(current_intensity)
                time.sleep(0.1)
                elapsed_time = time.time() - start_time

    def fade( self, start_intensity: list[int], end_intensity: list[int], duration_ms: int ) -> None:
        # Inicie uma nova thread apenas se a thread anterior estiver inativa
        if self._thread is not None or self._thread.is_alive():
            self.stop_thread()
        self._thread = threading.Thread( target = self._fade_thread, args = ( start_intensity, end_intensity, duration_ms ) )
        self._thread.start()

    def _pisca_thread(self, color: list[int], frequency: int ) -> None:
        while not self._stop_thread:
            self._rgb_queue.put(color)
            time.sleep(0.5 / frequency)
            self._rgb_queue.put([0, 0, 0])
            time.sleep(0.5 / frequency)

    def pisca(self, color: list[int], frequency: int ) -> None:
        # Inicie uma nova thread apenas se a thread anterior estiver inativa
        try:
            if self._thread is not None:
                self.stop_thread()
            elif self._thread.is_alive():
                self.stop_thread()
        except:
            pass
        self._thread = threading.Thread( target = self._pisca_thread, args = ( color, frequency, ) )
        self._thread.start()

    def get_current_intensity(self) -> list[int]:
        return [self.red_led.pwm_duty, self.green_led.pwm_duty, self.blue_led.pwm_duty]

    def update_color_from_queue(self) -> None:
        while not self._stop_thread:
            intensity = self._rgb_queue.get()
            self.set_color(intensity)
    
