#include<stdio.h>
#include <Arduino.h>
#include"sensor.h"
#include"config.h"

void initSensor(){
    // SỬA: Chuyển OUTPUT thành INPUT để đọc tín hiệu
    pinMode(s0, INPUT);
    pinMode(s1, INPUT);
    pinMode(s2, INPUT);
    pinMode(s3, INPUT);
    pinMode(s4, INPUT);
}

void errorCalculation(){
    l0=digitalRead(s0);
    l1=digitalRead(s1);
    l2=digitalRead(s2);
    l3=digitalRead(s3);
    l4=digitalRead(s4);
    //0-đen 1-trắng
    
    if(l0 == 1 && l1 == 1 && l2 == 1 && l3 == 1 && l4 == 0) {error=4; last_direction=1;}
    else if(l0 == 1 && l1 == 1 && l2 == 1 && l3 == 0 && l4 == 0) {error=3; last_direction=1;}
    else if(l0 == 1 && l1 == 1 && l2 == 1 && l3 == 0 && l4 == 1) {error=2; last_direction=1;}
    else if(l0 == 1 && l1 == 1 && l2 == 0 && l3 == 0 && l4 == 1) {error=1; last_direction=1;}
    else if(l0 == 1 && l1 == 1 && l2 == 0 && l3 == 1 && l4 == 1) error=0;
    else if(l0 == 1 && l1 == 0 && l2 == 0 && l3 == 1 && l4 == 1) {error=-1; last_direction=-1;}
    else if(l0 == 1 && l1 == 0 && l2 == 1 && l3 == 1 && l4 == 1) {error=-2; last_direction=-1;}
    else if(l0 == 0 && l1 == 0 && l2 == 1 && l3 == 1 && l4 == 1) {error=-3; last_direction=-1;}
    else if(l0 == 0 && l1 == 1 && l2 == 1 && l3 == 1 && l4 == 1) {error=-4; last_direction=-1;}
    
    // right-angle
    // LƯU Ý: Cần sửa điều kiện bên dưới nếu góc vuông trái khác với góc lệch -3 ở trên
    else if(l0 == 1 && l1 == 1 && l2 == 0 && l3 == 0 && l4 == 0) { error=100; }
    // else if(l0 == 0 && l1 == 0 && l2 == 0 && l3 == 1 && l4 == 1) { error=-100; } // Ví dụ sửa lại đk rẽ trái
    
    else if(l0 == 1 && l1 == 1 && l2 == 1 && l3 == 1 && l4 == 1) {
        // SỬA: Dùng toán tử gán "=" thay vì "=="
        if(last_direction == 1) error = 100; 
        else if(last_direction == -1) error = -100;
    }
}