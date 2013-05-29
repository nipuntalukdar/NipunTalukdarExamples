package org.nipun.bd.storm;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.net.NetworkInterface;
import java.util.Collections;
import java.util.Enumeration;

import org.hyperic.sigar.Sigar;
import org.hyperic.sigar.SigarException;

public class SystemInformation {
	private static Sigar nativeSigar = null;

	public SystemInformation() {
		nativeSigar = new Sigar();
	}

	long getProcessId() {
		return nativeSigar.getPid();
	}

	String getFQDN() {
		String host = null;
		host = getFirstEthIP();
		
		if (host == null) {
			try {
				host = nativeSigar.getFQDN();
			} catch (SigarException e) {
				try {
					host = Inet4Address.getLocalHost().getHostAddress();
				} catch (UnknownHostException e2) {
					host = "<Unable.to.get.hostname.haha>";
				}
			}
		}
		return host;
	}

	private String getFirstEthIP() {
		String ip = null;
		try {
			Enumeration<NetworkInterface> nets = NetworkInterface
					.getNetworkInterfaces();
			for (NetworkInterface netint : Collections.list(nets)) {
				if (!netint.getName().startsWith("eth"))
					continue;
				Enumeration<InetAddress> iadrs = netint.getInetAddresses();
				for (InetAddress iadr : Collections.list(iadrs)) {
					ip = iadr.getHostAddress();
					if (ip.indexOf(":") != -1)
						continue;
					break;
				}
				break;
			}
		} catch (SocketException e) {
			ip = null;
		}

		return ip;
	}

}
