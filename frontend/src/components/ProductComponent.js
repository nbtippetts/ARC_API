import React, {useState} from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import DeleteRoom from "./DeleteRoom";
import AddIP from "./AddIP";
import DeleteIP from "./DeleteIP";
import { Button, Stack, Card, CardHeader, CardActionArea, CardContent, Container,Typography,Grid} from '@mui/material';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import OpacityIcon from '@mui/icons-material/Opacity';
import ShowerIcon from '@mui/icons-material/Shower';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import Co2Icon from '@mui/icons-material/Co2';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import CloudIcon from '@mui/icons-material/Cloud';
import { makeStyles } from "@mui/styles";
import { styled } from '@mui/material/styles';
const useStyles = makeStyles(theme => ({
  overviewcard: {
    display:"flex",
	flexDirection: "column",
    justifyContent:"center",
  }
}));
const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));
const ProductComponent = () => {
	const products = useSelector((state) => state.allProducts.products);
	const ips = useSelector((state) => state.allIPS.ips);
	const classes = useStyles();
	const [expandedId, setExpandedId] = useState(-1);

	const handleExpandClick = (i) => {
		setExpandedId(expandedId === i ? -1 : i);
	};

	const renderList = products.map((product,index) => {
	console.log(product.name)
		return (
			<Card elevation={3}>
				<CardHeader action={
					<DeleteRoom roomId={product.id} indexId={index}/>
				} title={product.name} subheader={"Room "+product.id}></CardHeader>
				<CardContent>
				<Grid container spacing={2}>
				{product.ip.map((ip,ipIndex) => (
				<Grid item xs={12} sm={6} md={4}>
				<Card elevation={1} sx={{ minWidth: 275 }}>
					<CardActionArea>
					<CardHeader action={
						<DeleteIP ipId={ip.id} indexId={ipIndex} roomId={product.id} roomIndex={index}/>
					}
					title={ip.name}
					subheader={
						ip.name === "Climate" ? <CloudIcon/> :
						ip.name === "Temperature" ? <ThermostatIcon/> :
						ip.name === "Humidity" ? <OpacityIcon/> :
						ip.name === "CO2" ? <Co2Icon/> :
						ip.name === "Water" ? <ShowerIcon/> :
						ip.name === "Light" ? <LightbulbIcon/> : <QuestionMarkIcon/>
						}
					>
					</CardHeader>

					<CardContent className={classes.overviewcard}>
							<Typography
								className={"MuiTypography--headingflex"}
								variant={"h6"}
								gutterBottom>{ip.id}
								</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								variant={"caption"}>{ip.name}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								variant={"caption"}>{ip.state}
							</Typography>
							<Typography
								className={"MuiTypography--subheading"}
								variant={"caption"}>{ip.ip}
							</Typography>
							</CardContent>
							</CardActionArea>

					</Card>
				</Grid>
				))}
				</Grid>
				<Typography>
					<Link to={`/room/${product.id}`}>
						<Button variant="outlined">View</Button>
					</Link>
				</Typography>
				</CardContent>
				</Card>
		);
	});
	const ipList = ips.map((ipData,index) => {
		const { id, name, ip } = ipData;
		return (
				<Grid item xs={12} sm={6} md={4}>
				<Card elevation={3} sx={{ minWidth: 275 }}>
					<CardActionArea>
					<CardHeader
					title={name}
					subheader={
						name === "Climate" ? <CloudIcon/> :
						name === "Temperature" ? <ThermostatIcon/> :
						name === "Humidity" ? <OpacityIcon/> :
						name === "CO2" ? <Co2Icon/> :
						name === "Water" ? <ShowerIcon/> :
						name === "Light" ? <LightbulbIcon/> : <QuestionMarkIcon/>
						}
					>
					</CardHeader>
					<CardContent className={classes.overviewcard}>
					<ExpandMore
						expand={expandedId}
						onClick={() => handleExpandClick(index)}
						aria-expanded={expandedId === index}
						aria-label="show more"
					>
					<ExpandMoreIcon />
					</ExpandMore>
					</CardContent>
					</CardActionArea>
					<Collapse in={expandedId === index} timeout="auto" unmountOnExit>
						<CardContent>
						<AddIP ipId={id} indexId={index}/>
						</CardContent>
					</Collapse>
					</Card>
				</Grid>
		);
	});
	return(
		<Container maxWidth="lg">
		<Stack spacing={2}>
			<>{renderList}</>
			<Grid container spacing={2}>
				<>{ipList}</>
			</Grid>

		</Stack>
		</Container>
	)
};

export default ProductComponent;