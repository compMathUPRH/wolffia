
VERSION=$(shell grep Version ../debian/debiansrc/control | cut -d' ' -f2)



zip: ../dist
	cd .. ; make dist
	rm -Rf wolffia$(VERSION)
	mkdir wolffia$(VERSION)
	cp -R ../dist/* wolffia$(VERSION)
	zip -r wolffia$(VERSION).zip wolffia$(VERSION)

clean:
	rm -fR wolffia$(VERSION).zip
	rm -fR wolffia$(VERSION)
