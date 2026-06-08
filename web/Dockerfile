FROM ubuntu:22.04

# Menghindari prompt interaktif saat instalasi package
ENV DEBIAN_FRONTEND=noninteractive

# Install Apache, Python, dan mod_wsgi
RUN apt-get update && apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    libapache2-mod-wsgi-py3 \
    && apt-get clean

# Set direktori kerja
WORKDIR /var/www/padel

# Install dependensi Python
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Konfigurasi Apache VirtualHost
COPY padel.conf /etc/apache2/sites-available/padel.conf
RUN a2ensite padel.conf && a2dissite 000-default.conf

# Salin file WSGI dan aplikasi
COPY wsgi.py .
COPY app/ ./app/

# Berikan hak akses ke Apache
RUN chown -R www-data:www-data /var/www/padel

# Jalankan Apache di foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]