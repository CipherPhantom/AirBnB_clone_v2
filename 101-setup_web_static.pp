# sets up your web servers for the deployment of web_static.

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
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body></html>",
}

exec { 'rm link':
  command => 'rm -f /data/web_static/current',
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  require => Exec['rm link'],
}

exec { 'ubuntu':
  command => 'chown -R ubuntu:ubuntu /data/',
}

service {'nginx':
  ensure => 'running',
  enable => true,
}

file_line { 'nginx config':
  ensure   => 'present',
  path     => '/etc/nginx/sites-available/default',
  match    => '^}$',
  line     => "\n\tlocation /hbnb_static {\n\t\t alias /data/web_static/current/;\n\t}\n}",
  multiple => false,
  require  => Package['nginx'],
  notify   => Service['nginx'],
}
