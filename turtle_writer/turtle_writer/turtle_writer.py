import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import threading
import time
import math

def run_turtlesim_node(namespace):
    import subprocess
    subprocess.run(["ros2", "run", "turtlesim", "turtlesim_node", "--ros-args", "--remap", f"__ns:={namespace}"])

def draw_three(node, publisher):
     msg = Twist()
     
     
     msg.linear.x = 2.0
     msg.angular.z = 1.9 # 108 derece

     for _ in range(20):  # 3 sayısının alt kısmının çizimi
        publisher.publish(msg)
        time.sleep(0.1)

     msg.linear.x = 0.0
     msg.angular.z = -2.4   # -130 derece
     publisher.publish(msg) 

     for _ in range(15):  # 3 sayısının üst kısmı için gerekli dönüşün yapılması 
        publisher.publish(msg)
        time.sleep(0.1)

     msg.linear.x = 1.5
     msg.angular.z = 1.9 # 108 derece

     for _ in range(11):  # Sayının üst kısmının tamamlanması
        publisher.publish(msg)
        time.sleep(0.1)
    



def draw_Y(node, publisher):
    msg = Twist()

    for _ in range(3):
        # Y sayısının alt temelinin çizimi
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        publisher.publish(msg)
        time.sleep(1)  

        # Sonraki çizim için dönüş açılarının ayarı
        msg.linear.x = 0.0
        msg.angular.z = 0.7853981634  # Yaklaşık 45 derece
        publisher.publish(msg)
        time.sleep(1)  

        # Geriye kalan üst kısımları loop ile çizimi
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        publisher.publish(msg)
        time.sleep(1)  

        # Sonraki çizim için dönüş açılarının ayarı
        msg.linear.x = 0.0
        msg.angular.z = 3.1415926536  # Yaklaşık 180 derece
        publisher.publish(msg)
        time.sleep(1)  

    # Hareketin Sonu
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    publisher.publish(msg)


def draw_five(node, publisher):
    msg = Twist()
    msg.linear.x = 2.0
    msg.angular.z = 1.8 # Yaklaşık 103 derece

    # İlk yarım çemberi çizmek için
    for _ in range(20):
        publisher.publish(msg)
        time.sleep(0.1)

    # Sonraki çizim için dönüş açılarının ayarı
    msg.linear.x = 0.0
    msg.angular.z = -1.6 # -90 derece
    publisher.publish(msg)
    time.sleep(1.2)  

    
    msg.linear.x = 1.0
    msg.angular.z = 0.0
    for _ in range(10):
        publisher.publish(msg)
        time.sleep(0.1)

    # Sonraki çizim için dönüş açılarının ayarı
    msg.linear.x = 0.0
    msg.angular.z = -1.4  # Yaklaşık -90 derece
    publisher.publish(msg)
    time.sleep(1)  

    msg.linear.x = 1.0
    msg.angular.z = 0.0
    for _ in range(5):
        publisher.publish(msg)
        time.sleep(0.1)

def draw_B(node, publisher):
    time.sleep(15)
    msg = Twist()
    msg.linear.x = 2.5
    msg.angular.z = 1.8

    for _ in range(18):  # Çemberin tamamını dönmek için 30 adım yeterli olabilir
        publisher.publish(msg)
        time.sleep(0.1)

    msg.linear.x = 0.0
    msg.angular.z = -2.0   # -180 derece
    publisher.publish(msg)
    time.sleep(0.01)

    for _ in range(18):  # Yarı çemberin yarısını dönmek için 15 adım yeterli olabilir
        publisher.publish(msg)
        time.sleep(0.1)

    

    for _ in range(18):  # Çemberin tamamını dönmek için 30 adım yeterli olabilir
        msg.linear.x = 2.4
        msg.angular.z = 2.3
        publisher.publish(msg)
        time.sleep(0.1)
        
        
    msg.linear.x = 0.0
    msg.angular.z = 1.0
    publisher.publish(msg)
    time.sleep(1.5)

    

    for _ in range(13):  # Çemberin tamamını dönmek için 30 adım yeterli olabilir
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        publisher.publish(msg)
        time.sleep(0.1)
        
    

def main():
    rclpy.init()

    # Turtlesim düğümlerini ayrı thread'lerde başlat
    thread1 = threading.Thread(target=run_turtlesim_node, args=("/turtlesim1",))
    thread2 = threading.Thread(target=run_turtlesim_node, args=("/turtlesim2",))
    thread3 = threading.Thread(target=run_turtlesim_node, args=("/turtlesim3",))
    thread4 = threading.Thread(target=run_turtlesim_node, args=("/turtlesim4",))
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    
    # ROS node oluştur
    node = Node("shape_drawer")
    publisher_three = node.create_publisher(Twist, '/turtlesim1/turtle1/cmd_vel', 10)
    publisher_Y = node.create_publisher(Twist, '/turtlesim2/turtle1/cmd_vel', 10)
    publisher_five = node.create_publisher(Twist, '/turtlesim3/turtle1/cmd_vel', 10)
    publisher_B = node.create_publisher(Twist, '/turtlesim4/turtle1/cmd_vel', 10)
    
    # Şekilleri çizmek için thread'leri başlat
    thread_three = threading.Thread(target=draw_three, args=(node, publisher_three,))
    thread_Y = threading.Thread(target=draw_Y, args=(node, publisher_Y,))
    thread_five = threading.Thread(target= draw_five, args=(node, publisher_five,))
    thread_B = threading.Thread(target= draw_B, args=(node, publisher_B,))
    thread_Y.start()
    thread_three.start()
    thread_five.start()
    thread_B.start()

    # Thread'lerin tamamlanmasını bekle
    thread_Y.join()
    thread_three.join()
    thread_five.join()
    thread_B.join()

    # Turtlesim düğümlerinin kapanmasını bekle
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
