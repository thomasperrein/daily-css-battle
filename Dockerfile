FROM amazon/aws-lambda-python:3.12
# Install chrome dependencies
RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm jq unzip

RUN dnf install -y glibc-langpack-fr
ENV LANG=fr_FR.UTF-8
ENV LC_ALL=fr_FR.UTF-8
# Copy and run the chrome installer script
COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN rm ./chrome-installer.sh
# Install selenium
RUN pip install selenium requests bs4 python-dotenv
# Copy the main application code
COPY main.py ./
# Command to run the Lambda function
CMD [ "main.lambda_handler" ]