# ==========================================================================
# VERİ MADENCİLİĞİ VE MAKİNE ÖĞRENMESİ
# Python ile Temel Analitikten Büyük Veri ve Gerçek Zamanlı Sistemlere
# --------------------------------------------------------------------------
# Bölüm 12
# Konum : BÖLÜM 12: BÜYÜK VERİ ANALİTİĞİ VE DAĞITIK MAKİNE ÖĞRENMESİ › 12.2. Hadoop Ekosistemi ve MapReduce Mantığı › 12.2.1. HDFS: Hadoop Dağıtık Dosya Sistemi › Python ile HDFS Etkileşimi: hdfs3 ve PyArrow
# Kitap  : Kod 12.1 (Python ile HDFS dosya işlemleri)
# Dosya : bolum12/12_02_01_python-ile-hdfs-etkilesimi-hdfs3-ve-pyarrow-2.sh
# ==========================================================================
hdfs = pafs.HadoopFileSystem(host='namenode-host', port=8020)
