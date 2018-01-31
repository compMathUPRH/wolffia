
VERSION=$(shell grep Version ../debian/debiansrc/control | cut -d' ' -f2)


all:
	echo "Nothing done"

wolffia_$(VERSION)-1.rpm: ../debian/wolffia_$(VERSION)-1_all.deb
	mkdir -p ./rpmbuild/BUILD
	mkdir -p ./rpmbuild/SPECS
	cp -R ../dist ./rpmbuild/BUILD
	cp ./rpmsrc/wolffia-$(VERSION)-1.spec ./rpmbuild/SPECS
	cd ./rpmbuild/SPECS;rpmbuild -bb wolffia-$(VERSION)-1.spec

../debian/wolffia_$(VERSION)-1_all.deb:
	cd .. ; make debian

clean:
	rm -fR ./rpmbuild
	rm -fR wolffia-$(VERSION)-1.rpm
