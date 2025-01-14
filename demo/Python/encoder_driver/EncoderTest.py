#!/usr/bin/python
# import Emakefun_MotorHAT, Emakefun_DCMotor, Raspi_Stepper
import subprocess

import RPi.GPIO as GPIO
import serial
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from wheels_drivers.encoder_driver.Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_StepperMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(0x60, 50, False)
# GPIO.setmode(GPIO.BOARD)


servo = mh.getServo(1)

encoder1 = mh.getEncoder(1)
encoder2 = mh.getEncoder(2)
encoder3 = mh.getEncoder(3)
encoder4 = mh.getEncoder(4)

# B右前 A左后 C右后 D左前
# C
encoderC_IN1pin = encoder1.IN2pin
encoderC_IN2pin = encoder1.IN1pin
encoderC_PWM1pin = encoder1.PWM1pin
encoderC_PWM2pin = encoder1.PWM2pin
# B
encoderB_IN1pin = encoder3.IN2pin
encoderB_IN2pin = encoder3.IN1pin
encoderB_PWM1pin = encoder2.PWM1pin
encoderB_PWM2pin = encoder2.PWM2pin
# D
encoderD_IN1pin = encoder2.IN1pin
encoderD_IN2pin = encoder2.IN2pin
encoderD_PWM1pin = encoder3.PWM1pin
encoderD_PWM2pin = encoder3.PWM2pin
# A
encoderA_IN1pin = encoder4.IN1pin
encoderA_IN2pin = encoder4.IN2pin
encoderA_PWM1pin = encoder4.PWM1pin
encoderA_PWM2pin = encoder4.PWM2pin


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)


def get_data():
    while True:
        try:
            ser = serial.Serial('/dev/ttyAMA0', 115200, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, 1)

            if not ser.isOpen:
                ser.open()  # 打开串口

            try:
                while True:
                    size = ser.inWaiting()  # 获得缓冲区字符
                    # print('-', end='')
                    if size != 0:
                        data = ser.read(size)  # 读取内容并显示
                        data = data.decode('unicode_escape')

                        try:
                            temp_data = data[data.index('s') + 1:data.index('s') + 52]
                            temp_list = [i for i in temp_data.split()]
                            # print(temp_data)
                            if len(temp_list) == 4:
                                if all([len(i) == 12 for i in temp_list]):
                                    # print(temp_list)
                                    return temp_list
                                else:
                                    pass
                                    # print("5!")
                            else:
                                print(temp_list)
                                print("4!error")
                        except Exception as e:
                            # print(data)
                            # print('1!', end='')
                            if str(e) != """substring not found""" and str(e) != "list index out of range":
                                print(1, e)
                        # print(data)
                        # print(data.decode('utf-8','replace'))
                        # print(res.decode('unicode_escape'))
                    ser.flushInput()  # 情况接收缓存区
                    time.sleep(0.01)
            except KeyboardInterrupt:
                ser.close()
        except Exception as e:
            print('2!', end='')
            if str(e) != "[Errno 13] could not open port /dev/ttyAMA0: [Errno 13] Permission denied: '/dev/ttyAMA0'" and str(
                    e) != "[Errno 5] Input/output error":
                print(2, e)
            subprocess.Popen("echo 'ztyivc' |sudo -S  chmod 777 /dev/ttyAMA0 ", shell=True, stdout=subprocess.PIPE)
            # time.sleep(0.05)


def set_Servo(angle):
    if angle == 'A' or angle == 1:
        servo.writeServo(0)
    elif angle == 'B' or angle == 3:
        servo.writeServo(47)
    elif angle == 'C' or angle == 2:
        servo.writeServo(95)
    elif angle == 'D' or angle == 4:
        servo.writeServo(142)


def run_To(direction, speed=4095):
    # 前
    if direction == 'A' or direction == 1:
        mh.setPWM(encoderB_IN1pin, speed)
        mh.setPWM(encoderB_IN2pin, 0)
        mh.setPWM(encoderD_IN1pin, speed)
        mh.setPWM(encoderD_IN2pin, 0)
    # 后
    elif direction == 'B' or direction == 2:
        mh.setPWM(encoderB_IN1pin, 0)
        mh.setPWM(encoderB_IN2pin, speed)
        mh.setPWM(encoderD_IN1pin, 0)
        mh.setPWM(encoderD_IN2pin, speed)
    # 左
    elif direction == 'C' or direction == 3:
        mh.setPWM(encoderA_IN1pin, 0)
        mh.setPWM(encoderA_IN2pin, speed)
        mh.setPWM(encoderC_IN1pin, 0)
        mh.setPWM(encoderC_IN2pin, speed)
    # 右
    elif direction == 'D' or direction == 4:
        mh.setPWM(encoderA_IN1pin, speed)
        mh.setPWM(encoderA_IN2pin, 0)
        mh.setPWM(encoderC_IN1pin, speed)
        mh.setPWM(encoderC_IN2pin, 0)

    elif direction == 5:
        mh._pwm.setPWM(encoderA_IN1pin, 0, 4096)
        mh._pwm.setPWM(encoderA_IN2pin, 0, 4096)
        mh._pwm.setPWM(encoderC_IN1pin, 0, 4096)
        mh._pwm.setPWM(encoderC_IN2pin, 0, 4096)
        mh._pwm.setPWM(encoderB_IN1pin, 0, 4096)
        mh._pwm.setPWM(encoderB_IN2pin, 0, 4096)
        mh._pwm.setPWM(encoderD_IN1pin, 0, 4096)
        mh._pwm.setPWM(encoderD_IN2pin, 0, 4096)
    # x右
    elif direction == 6:
        mh.setPWM(encoderB_IN1pin, speed)
        mh.setPWM(encoderB_IN2pin, 0)
        mh.setPWM(encoderD_IN1pin, 0)
        mh.setPWM(encoderD_IN2pin, speed)
    # x左
    elif direction == 7:
        mh.setPWM(encoderB_IN1pin, 0)
        mh.setPWM(encoderB_IN2pin, speed)
        mh.setPWM(encoderD_IN1pin, speed)
        mh.setPWM(encoderD_IN2pin, 0)
    # y右
    elif direction == 8:
        mh.setPWM(encoderA_IN1pin, speed)
        mh.setPWM(encoderA_IN2pin, 0)
        mh.setPWM(encoderC_IN1pin, 0)
        mh.setPWM(encoderC_IN2pin, speed)
    # y左
    elif direction == 9:
        mh.setPWM(encoderA_IN1pin, 0)
        mh.setPWM(encoderA_IN2pin, speed)
        mh.setPWM(encoderC_IN1pin, speed)
        mh.setPWM(encoderC_IN2pin, 0)


# 1 2 B D
# 3 4 A C
import RPi.GPIO as GPIO

from wheels_drivers.encoder_driver.EncoderTest import encoderB_PWM1pin, encoderB_PWM2pin, encoderC_PWM1pin, \
    encoderC_PWM2pin, encoderA_PWM1pin, encoderA_PWM2pin, encoderD_PWM1pin, encoderD_PWM2pin, run_To, turnOffMotors

turnOffMotors()


def is_reset():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    reset = 0
    if GPIO.input(9) == 1:  # 按下（该按键模块，当松开的时候是低电平，按下时高电平）
        time.sleep(0.02)  # 延时20ms  绕过抖动区间，为了防抖
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if (GPIO.input(9) == 1):  # 再次判断是否在按下的状态(判断是否在稳定区间)
            buzz()
            time.sleep(1)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            if (GPIO.input(9) == 1):
                buzz()
                reset = 2
            else:
                reset = 1
            time.sleep(1)

    GPIO.cleanup()

    return reset


def buzz():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

    for i in range(200):
        time.sleep(0.0001)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(27, GPIO.LOW)

    GPIO.cleanup()


def correct_local(run, run_pwm=4095, correct_direction=-1):
    temp_list = get_data()
    a = temp_list[0]
    b = temp_list[1]
    c = temp_list[2][::-1]
    d = temp_list[3][::-1]
    if correct_direction == -1:
        # 先平移纠偏，再旋转纠偏
        if a[6:8] != "11" or c[6:8] != "11":
            a_l = a.find("1") + 1
            a_r = a.rfind("1") + 1
            c_l = c.find("1") + 1
            c_r = c.rfind("1") + 1
            if a_r != 0 and a_l != 0 and c_r != 0 and c_l != 0:
                dart_a = (a_l + a_r) / 2.0 - 6.5
                dart_c = (c_l + c_r) / 2.0 - 6.5
                if dart_c > 0.4 or dart_c < -0.4 or dart_a > 0.4 or dart_a < -0.4:
                    pwm_a = int(dart_a * 1000)
                    pwm_c = int(dart_c * 1000)
                    print(dart_a, pwm_a, dart_c, pwm_c)
                    if pwm_c > 0:
                        mh.setPWM(encoderC_IN1pin, 0)
                        mh.setPWM(encoderC_IN2pin, pwm_c)
                    else:
                        mh.setPWM(encoderC_IN1pin, -pwm_c)
                        mh.setPWM(encoderC_IN2pin, 0)
                    if pwm_a > 0:
                        mh.setPWM(encoderA_IN1pin, 0)
                        mh.setPWM(encoderA_IN2pin, pwm_a)
                    else:
                        mh.setPWM(encoderA_IN1pin, -pwm_a)
                        mh.setPWM(encoderA_IN2pin, 0)
                time.sleep(0.1)
                run_To(5)
                run_To(run, run_pwm)
                # place = (a_l + c_l + a_r + c_r) / 4.0
                # a_x = (a_l + a_r) / 2.0
                # c_x = (c_l + c_r) / 2.0
                # dart_r = a_x - c_x
                # dart = place - 6.5
                # print('dart_r：', dart_r, 'dart:', dart)
                # if dart_r > 0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(9, 900)
                #     time.sleep(0.1)
                #     run_To(9, 0)
                #     run_To(run, run_pwm)
                # elif dart_r < -0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(8, 900)
                #     time.sleep(0.1)
                #     run_To(8, 0)
                #     run_To(run, run_pwm)
                # elif dart > 0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(3, 900)
                #     time.sleep(0.1)
                #     run_To(3, 0)
                #     run_To(run, run_pwm)
                # elif dart < -0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(4, 900)
                #     time.sleep(0.1)
                #     run_To(4, 0)
                #     run_To(run, run_pwm)
                # # print(place)

            else:
                # print("3_1!,为y轴行走", end='')
                pass

        if c[6:8] != "11" or d[6:8] != "11":
            b_l = b.find("1") + 1
            b_r = b.rfind("1") + 1
            d_l = d.find("1") + 1
            d_r = d.rfind("1") + 1
            if b_r != 0 and b_l != 0 and d_r != 0 and d_l != 0:
                dart_b = (b_l + b_r) / 2.0 - 6.5
                dart_d = (d_l + d_r) / 2.0 - 6.5
                if dart_b > 0.4 or dart_b < -0.4 or dart_d > 0.4 or dart_d < -0.4:
                    pwm_b = int(dart_b * 1000)
                    pwm_d = int(dart_d * 1000)
                    if pwm_b > 0:
                        mh.setPWM(encoderB_IN1pin, 0)
                        mh.setPWM(encoderB_IN2pin, pwm_b)
                    else:
                        mh.setPWM(encoderB_IN1pin, -pwm_b)
                        mh.setPWM(encoderB_IN2pin, 0)
                    if pwm_d > 0:
                        mh.setPWM(encoderD_IN1pin, 0)
                        mh.setPWM(encoderD_IN2pin, pwm_d)
                    else:
                        mh.setPWM(encoderD_IN1pin, -pwm_d)
                        mh.setPWM(encoderD_IN2pin, 0)
                time.sleep(0.1)
                run_To(5)
                run_To(run, run_pwm)
                # place = (b_l + b_l + d_r + d_r) / 4.0
                # b_x = (b_l + b_r) / 2.0
                # d_x = (d_l + d_r) / 2.0
                # dart_r = b_x - d_x
                # dart = place - 6.5
                # print('dart_r：', dart_r, 'dart:', dart)
                # if dart_r > 0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(7, 900)
                #     time.sleep(0.1)
                #     run_To(7, 0)
                #     run_To(run, run_pwm)
                # elif dart_r < -0.4:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(6, 900)
                #     time.sleep(0.1)
                #     run_To(6, 0)
                #     run_To(run, run_pwm)
                # elif dart > 0.5:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(2, 900)
                #     time.sleep(0.1)
                #     run_To(2, 0)
                #     run_To(run, run_pwm)
                # elif dart < -0.5:
                #     run_To(run, int(run_pwm / 2))
                #     run_To(1, 900)
                #     time.sleep(0.1)
                #     run_To(1, 0)
                #     run_To(run, run_pwm)
                # # print(place)
            else:
                pass
                # print("3_2!,为x轴行走", end='')
    elif correct_direction == 'a' or correct_direction == 1:
        if a[6:8] != "11":
            a_l = a.find("1") + 1
            a_r = a.rfind("1") + 1
            dart_a_x = (a_l + a_r) / 2.0 - 6.5
            if a_l != 0 and a_r != 0:
                if dart_a_x < -0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(4, 900)
                    time.sleep(0.1)
                    run_To(4, 0)
                    run_To(run, run_pwm)
                elif dart_a_x > 0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(3, 900)
                    time.sleep(0.1)
                    run_To(3, 0)
                    run_To(run, run_pwm)
    elif correct_direction == 'c' or correct_direction == 2:
        if c[6:8] != "11":
            c_l = c.find("1") + 1
            c_r = c.rfind("1") + 1
            dart_c_x = (c_l + c_r) / 2.0 - 6.5
            if c_l != 0 and c_r != 0:
                if dart_c_x < -0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(4, 900)
                    time.sleep(0.1)
                    run_To(4, 0)
                    run_To(run, run_pwm)
                elif dart_c_x > 0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(3, 900)
                    time.sleep(0.1)
                    run_To(3, 0)
                    run_To(run, run_pwm)
    elif correct_direction == 'b' or correct_direction == 3:
        if b[6:8] != "11":
            b_l = b.find("1") + 1
            b_r = b.rfind("1") + 1
            dart_b_x = (b_l + b_r) / 2.0 - 6.5
            if b_l != 0 and b_r != 0:
                if dart_b_x < -0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(1, 900)
                    time.sleep(0.1)
                    run_To(1, 0)
                    run_To(run, run_pwm)
                elif dart_b_x > 0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(2, 900)
                    time.sleep(0.1)
                    run_To(2, 0)
                    run_To(run, run_pwm)
    elif correct_direction == 'd' or correct_direction == 4:
        if d[6:8] != "11":
            d_l = d.find("1") + 1
            d_r = d.rfind("1") + 1
            dart_d_x = (d_l + d_r) / 2.0 - 6.5
            if d_l != 0 and d_r != 0:
                if dart_d_x < -0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(1, 900)
                    time.sleep(0.1)
                    run_To(1, 0)
                    run_To(run, run_pwm)
                elif dart_d_x > 0.5:
                    run_To(run, int(run_pwm / 2))
                    run_To(2, 900)
                    time.sleep(0.1)
                    run_To(2, 0)
                    run_To(run, run_pwm)


def turnAround(step, distance, is_buzz=True, run_pwm=900):
    # 0 动力起步 位移14.5cm
    # 如果需要精准控制 需要在调用前反向制动 并停止
    distance = int(distance / 100 * 5000)

    # 前
    if step == 1:
        globalCounter = 0
        flag = 0
        Last_RoB_Status = 0
        Current_RoB_Status = 0

        pin1_a = encoderB_PWM1pin
        pin1_b = encoderB_PWM2pin
        pin2_a = encoderD_PWM1pin
        pin2_b = encoderD_PWM2pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1_a, GPIO.IN)
        GPIO.setup(pin1_b, GPIO.IN)
        GPIO.setup(pin2_a, GPIO.IN)
        GPIO.setup(pin2_b, GPIO.IN)

        run_To(1, run_pwm)
        while True:
            # correct_local(1, run_pwm)
            Last_RoB_Status = GPIO.input(pin1_b)
            while (not GPIO.input(pin1_a)):  # 未旋转时，GPIO.input(pin1_a)值为1，旋转时会变为0
                Current_RoB_Status = GPIO.input(pin1_b)  # 旋转时的当前值
                flag = 1
                # print(GPIO.input(pin1_a))
            if flag == 1:
                flag = 0
                if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                    globalCounter = globalCounter - 1  # 顺时针旋转，角位移增大
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                    globalCounter = globalCounter + 1  # 逆时针旋转，数值减小
            if globalCounter >= distance:
                run_To(2, run_pwm)
                time.sleep(0.03)
                turnOffMotors()
                if is_buzz:
                    buzz()
                break
            # print(globalCounter)
    # 后
    elif step == 2:
        globalCounter = 0
        flag = 0
        Last_RoB_Status = 0
        Current_RoB_Status = 0

        pin1_a = encoderB_PWM1pin
        pin1_b = encoderB_PWM2pin
        pin2_a = encoderD_PWM1pin
        pin2_b = encoderD_PWM2pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1_a, GPIO.IN)
        GPIO.setup(pin1_b, GPIO.IN)
        GPIO.setup(pin2_a, GPIO.IN)
        GPIO.setup(pin2_b, GPIO.IN)

        run_To(2, run_pwm)
        while True:
            # correct_local(2, run_pwm)
            Last_RoB_Status = GPIO.input(pin1_b)
            while (not GPIO.input(pin1_a)):  # 未旋转时，GPIO.input(pin1_a)值为1，旋转时会变为0
                Current_RoB_Status = GPIO.input(pin1_b)  # 旋转时的当前值
                flag = 1
                # print(GPIO.input(pin1_a))
            if flag == 1:
                flag = 0
                if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                    globalCounter = globalCounter - 1  # 顺时针旋转，角位移增大
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                    globalCounter = globalCounter + 1  # 逆时针旋转，数值减小
            if globalCounter <= -distance:
                run_To(1, run_pwm)
                time.sleep(0.03)
                turnOffMotors()
                if is_buzz:
                    buzz()
                break
            # print(globalCounter)
    # 左
    elif step == 3:
        globalCounter = 0
        flag = 0
        Last_RoB_Status = 0
        Current_RoB_Status = 0

        pin1_a = encoderA_PWM1pin
        pin1_b = encoderA_PWM2pin
        pin2_a = encoderC_PWM1pin
        pin2_b = encoderC_PWM2pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1_a, GPIO.IN)
        GPIO.setup(pin1_b, GPIO.IN)
        GPIO.setup(pin2_a, GPIO.IN)
        GPIO.setup(pin2_b, GPIO.IN)

        run_To(3, run_pwm)
        while True:
            # correct_local(3, run_pwm)
            Last_RoB_Status = GPIO.input(pin2_b)
            while (not GPIO.input(pin2_a)):  # 未旋转时，GPIO.input(pin1_a)值为1，旋转时会变为0
                Current_RoB_Status = GPIO.input(pin2_b)  # 旋转时的当前值
                flag = 1
                # print(GPIO.input(pin1_a))
            if flag == 1:
                flag = 0
                if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                    globalCounter = globalCounter + 1  # 顺时针旋转，角位移增大
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                    globalCounter = globalCounter - 1  # 逆时针旋转，数值减小
            if globalCounter >= distance:
                run_To(4, run_pwm)
                time.sleep(0.03)
                turnOffMotors()
                if is_buzz:
                    buzz()
                break
            # print(globalCounter)
    # 右
    elif step == 4:
        globalCounter = 0
        flag = 0
        Last_RoB_Status = 0
        Current_RoB_Status = 0

        pin1_a = encoderA_PWM1pin
        pin1_b = encoderA_PWM2pin
        pin2_a = encoderC_PWM1pin
        pin2_b = encoderC_PWM2pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1_a, GPIO.IN)
        GPIO.setup(pin1_b, GPIO.IN)
        GPIO.setup(pin2_a, GPIO.IN)
        GPIO.setup(pin2_b, GPIO.IN)

        run_To(4, run_pwm)
        while True:
            # correct_local(4, run_pwm)
            Last_RoB_Status = GPIO.input(pin2_b)
            while (not GPIO.input(pin2_a)):  # 未旋转时，GPIO.input(pin1_a)值为1，旋转时会变为0
                Current_RoB_Status = GPIO.input(pin2_b)  # 旋转时的当前值
                flag = 1
                # print(GPIO.input(pin1_a))
            if flag == 1:
                flag = 0
                if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                    globalCounter = globalCounter + 1  # 顺时针旋转，角位移增大
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                    globalCounter = globalCounter - 1  # 逆时针旋转，数值减小
            if globalCounter <= -distance:
                run_To(3, run_pwm)
                time.sleep(0.03)
                turnOffMotors()
                if is_buzz:
                    buzz()
                break
            # print(globalCounter)
    else:
        print("step值超出范围")
    # GPIO.cleanup()


atexit.register(turnOffMotors)

turnOffMotors()

# run_To(4)
if __name__ == '__main__':
    turnOffMotors()
    set_Servo(1)

    # 0 动力起步 位移14.5cm
    # 如果需要精准控制 需要在调用前反向制动 并停止
    # distance = int(distance / 100 * 5000)

    # # 前
    # globalCounter = 0
    # flag = 0
    # Last_RoB_Status = 0
    # Current_RoB_Status = 0
    # pinA_a = encoderA_PWM1pin
    # pinA_b = encoderA_PWM2pin
    # pinB_a = encoderB_PWM1pin
    # pinB_b = encoderB_PWM2pin
    # pinC_a = encoderC_PWM1pin
    # pinC_b = encoderC_PWM2pin
    # pinD_a = encoderD_PWM1pin
    # pinD_b = encoderD_PWM2pin
    #
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pinA_a, GPIO.IN)
    # GPIO.setup(pinA_b, GPIO.IN)
    # GPIO.setup(pinB_a, GPIO.IN)
    # GPIO.setup(pinB_b, GPIO.IN)
    # GPIO.setup(pinC_a, GPIO.IN)
    # GPIO.setup(pinC_b, GPIO.IN)
    # GPIO.setup(pinD_a, GPIO.IN)
    # GPIO.setup(pinD_b, GPIO.IN)
    #
    # while 1:
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setup(pinA_a, GPIO.IN)
    #     GPIO.setup(pinA_b, GPIO.IN)
    #     GPIO.setup(pinB_a, GPIO.IN)
    #     GPIO.setup(pinB_b, GPIO.IN)
    #     GPIO.setup(pinC_a, GPIO.IN)
    #     GPIO.setup(pinC_b, GPIO.IN)
    #     GPIO.setup(pinD_a, GPIO.IN)
    #     GPIO.setup(pinD_b, GPIO.IN)
    #     print(GPIO.input(pinC_b))
    #     Last_RoB_Status = GPIO.input(pinC_b)
    #     while (not GPIO.input(pinC_a)):  # 未旋转时，GPIO.input(pin1_a)值为1，旋转时会变为0
    #         Current_RoB_Status = GPIO.input(pinC_b)  # 旋转时的当前值
    #         flag = 1
    #         # print(GPIO.input(pin1_a))
    #     if flag == 1:
    #         flag = 0
    #         if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
    #             globalCounter = globalCounter - 1  # 顺时针旋转，角位移增大
    #         if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
    #             globalCounter = globalCounter + 1  # 逆时针旋转，数值减小
    #         print(globalCounter)
