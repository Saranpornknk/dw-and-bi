# Building a Data Lake

เพื่อให้เราสามารถสร้างไฟล์ได้จาก Jupyter Lab ให้รันคำสั่งด้านล่างนี้

```sh
sudo chmod 777 .
```

แล้วค่อยรัน

```sh
docker-compose up
```

# Data Lake
Data Lake คือที่เก็บขนาดใหญ่ที่สามารถเก็บข้อมูลได้ทุกรูปแบบจากหลายแหล่งโดยที่ไม่ต้องมีการแปลงข้อมูลก่อน พูดให้เข้าใจง่ายๆก็คือสามารถเก็บข้อมูลดิบได้ ตั้งแต่ข้อมูลที่มีโครงสร้างชัดเจน (Structured Data) ข้อมูลกึ่งโครงสร้าง (Semi-Structured Data) และข้อมูลที่ไม่มีโครงสร้างแน่นอน (Unstructured Data)
ตัวอย่างเทคโนโลยี Data Lake เช่น Azure Data Lake Storage, Amazon S3


# PySpark

**PySpark is the Python API for Apache Spark, an open source, distributed computing framework and set of libraries for real-time, large-scale data processing. If you’re already familiar with Python and libraries such as Pandas, then PySpark is a good language to learn to create more scalable analyses and pipelines.**

Ref: https://domino.ai/data-science-dictionary/pyspark