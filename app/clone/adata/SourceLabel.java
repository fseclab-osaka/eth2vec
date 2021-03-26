package ca.mcgill.sis.dmas.kam1n0.app.clone.adata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;

public class SourceLabel {
	@JsonIgnore
	public Map<String, ContractLabel> srcLabel = new HashMap<>();
	//public VulnsList source;

	@JsonAnyGetter
	public Map<String, ContractLabel> getVulns() {
		return this.srcLabel;
	}

	@JsonAnySetter
	public void setVulns(String srcName, ContractLabel cnt) {
		this.srcLabel.put(srcName,  cnt);
	}

	public List<String> getSrcNames() {
		List<String> keyList = new ArrayList<>();
		for(String key : srcLabel.keySet()) {
			keyList.add(key);
		}
		return keyList;
	}
	public ContractLabel getSource(String key) {
		return srcLabel.get(key);
	}

}
