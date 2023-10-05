# sets up your web servers for the deployment of web_static.

$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
	add_header X-Served-By ${hostname};
    
	root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      internal;
    }
}"

exec { 'apt update':
  command => '/usr/bin/apt-get update',
}

package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt update'],
}

file { '/data/web_static/releases/test/':
  ensure  => 'directory',
  recurse => true,
}

file { '/data/web_static/shared/':
  ensure  => 'directory',
  recurse => true,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School\n",
}


file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
}

exec { 'ubuntu':
  command => 'chown -R ubuntu:ubuntu /data/',
}

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School\n",
  require => Package['nginx'],
}

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
  require => Package['nginx'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
  require => Package['nginx'],
}

service {'nginx':
  ensure => 'running',
  enable => true,
}
