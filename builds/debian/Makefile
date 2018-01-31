
VERSION=$(shell grep Version debiansrc/control | cut -d' ' -f2)

wolffia_$(VERSION)_all.deb: ../dist
	cd .. ; make dist
	mkdir -p ./debian/usr/bin
	mkdir -p ./debian/usr/share/wolffia
	mkdir -p ./debian/usr/share/doc/wolffia
	mkdir -p ./debian/usr/share/applications
	mkdir -p debian/DEBIAN
	cp ./debiansrc/copyright ./debian/usr/share/doc/wolffia
	cp -R ../dist/* ./debian/usr/share/wolffia
	ln -fs /usr/share/wolffia/wolffia.py ./debian/usr/bin/wolffia
	find ./debian -type d | xargs chmod 755 
	cp debiansrc/control debiansrc/prerm debiansrc/postinst ./debian/DEBIAN
	cp debiansrc/wolffia.desktop ./debian/usr/share/applications
	fakeroot dpkg-deb --build debian
	mv debian.deb wolffia_$(VERSION)_all.deb

clean:
	rm -fR ./debian
	rm -fR wolffia_$(VERSION)_all.deb
