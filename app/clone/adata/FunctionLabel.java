package ca.mcgill.sis.dmas.kam1n0.app.clone.adata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

public class FunctionLabel {
	@JsonIgnore
	public Map<String, VulnsList> funcLabel = new HashMap<>();
	//public Map<String, VulnsList> contract = new HashMap<>();

	@JsonAnyGetter
	public Map<String, VulnsList> getVulns() {
		return this.funcLabel;
	}

	@JsonAnySetter
	public void setVulns(String funcName, VulnsList vulns) {
		this.funcLabel.put(funcName,  vulns);
	}

	public List<String> getFuncNames() {
		List<String> keyList = new ArrayList<>();
		for(String key : funcLabel.keySet()) {
			keyList.add(key);
		}
		return keyList;
	}
	public VulnsList getFunction(String key) {
		return funcLabel.get(key);
	}

}
