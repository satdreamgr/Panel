#!/bin/sh
cd /tmp
echo -------------------------------------------------------------------------
echo $1
echo -------------------------------------------------------------------------
case $1 in
############# update #############
"create")
cd /etc/enigma2
if grep -q greekstreamtv.tv bouquets.tv
then
  echo "Service name already installed,  Download Update Bouquet Liste..."
   else
    echo "Service name installed, Update Bouquet Liste... "
  sed -i '2i #SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.greekstreamtv.tv" ORDER BY bouquet' bouquets.tv
fi
    ;;

*)
    echo "error"
    ;;
esac
exit 0


