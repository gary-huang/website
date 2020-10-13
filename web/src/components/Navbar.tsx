import { Box, Button, makeStyles, Menu, MenuItem } from '@material-ui/core'
import AppBar from '@material-ui/core/AppBar'
import { common } from '@material-ui/core/colors'
import Toolbar from '@material-ui/core/Toolbar'
import React from 'react'
import { MenuTab } from './MenuTab'

const useStyles = makeStyles({
	navbar: {
		background: common.white,
	},
	toolbar: {
		display: 'flex',
		justifyContent: 'space-between',
	},
	image: {
		maxWidth: '100px',
	},
	tabs: {
		color: common.black,
		display: 'flex',
	},
})

type NavbarProps = {}
export const Navbar: React.FC<NavbarProps> = () => {
	const classes = useStyles()
	return (
		<AppBar className={classes.navbar}>
			<Toolbar className={classes.toolbar}>
				<Box ml={2}>
					<img src="/static/img/crossroads.png" className={classes.image} />
				</Box>
				<Box className={classes.tabs}>
					<MenuTab
						name="Connecting"
						pages={['Example 1', 'Example 2']}
					></MenuTab>
					<MenuTab name="Contact Us" pages={['Office', 'Directions']}></MenuTab>
				</Box>
			</Toolbar>
		</AppBar>
	)
}
