FROM jboss/keycloak

ARG URL_PATH

USER jboss 
RUN sed -i -e 's|<web-context>auth</web-context>|<web-context>'${URL_PATH}auth'</web-context>|' $JBOSS_HOME/standalone/configuration/standalone.xml
RUN sed -i -e 's|<web-context>auth</web-context>|<web-context>'${URL_PATH}auth'</web-context>|' $JBOSS_HOME/standalone/configuration/standalone-ha.xml
RUN sed -i -e 's|name="/"|name="'${URL_PATH}'"|' $JBOSS_HOME/standalone/configuration/standalone.xml
RUN sed -i -e 's|name="/"|name="'${URL_PATH}'"|' $JBOSS_HOME/standalone/configuration/standalone-ha.xml
RUN sed -i -e 's|/auth|'/${URL_PATH}auth'|' $JBOSS_HOME/welcome-content/index.html
