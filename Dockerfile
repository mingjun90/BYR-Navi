FROM ruby:2.4.2

RUN apt-get update && apt-get install -y python2.7 python-pip --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV APP_HOME /app
ENV HOME /

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY Gemfile $APP_HOME/
COPY Gemfile.lock $APP_HOME/

RUN bundle install

COPY . $APP_HOME
COPY ./navi.sh $HOME

EXPOSE 5000

CMD ["bash", "/navi.sh"]
