How to install for Maya
1. Go to "C:\Users\{Your PC username}\Documents\maya\scripts".
2. Create folder name "asser_viewer".
3. Extract "asset_viewer-main.zip" into asser_viewer folder and don't forget to delete "-main" after extract file.
4. open "maya_shelf_button.py" in script edit and save into shelf

วิธีการติดตั้งสำหรับ Maya
1. ไปที่โฟลเดอร์ Documents > maya > scripts
2. สร้างโฟลเดอร์ชื่อ "asser_viewer"
3. แตกไฟล์ "asset_viewer-main.zip" ลงไปในโฟลเดอร์ที่สร้างขึ้น และหลังแตกไฟล์แล้วให้ลบ "-main" ออกจากชื่อโฟลเดอร์ด้วย
4. ไปที่ script editor เปิดไฟล์ "maya_shelf_button.py" แล้ว save into shelf

วิธีติดตั้งสำหรับ Blender
ก่อนอื่นต้องติดตั้ง PySide6 ก่อน
1.ไปที่หน้าแทบ "Scripting" แล้วพิมพ์ "bpy.utils.user_resource("SCRIPTS", path = "modules")" ลงในช่อง command line
2.copy path ที่ได้ แล้วพิมพ์คำสั่ง "python.exe -m pip install pyside6 --target="path ที่ copy" " ลงใน Notepad
3.เปิด Command Prompt แล้วไปที่ "C:\Program Files\Blender Foundation\Blender x.x\x.x\python\bin" เช่น ให้พิมพ์ cd C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin
4.เอา command ที่เตรียมไว้ใน Notepad ลงไปแล้วรันคำสั่งนั้น
5.หากยังหาวิธีลง PySide6 ไม่ได้ให้เพิ่งพา Google ละ
6.รันคำสั่งใน "blender_shelf_button.py"
